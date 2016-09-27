import sys
import re
import readline
import tempfile
import subprocess
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from notes.models import Document, Note
from projects.models import Project
from languages.models import Language
from lexical_units.models import LexicalUnit, LexicalPattern
import lexical_units.utils as lex
#from projects.helpers import project_name_is_valid
import cli.utils.projects as prj
import languages.utils as lang
from qiq.common import SUCCESS, INVALID, EXISTS, NOT_FOUND
from termblocks import TableBlock
from cli.config import read_config_file

import shlex

# Document's name begin with a letter, may contain numbers and dots, cannot end
# with a dot. All letters are lower case.
DOCNAME_re = re.compile(r'^[a-z][a-z0-9]*(?:\.[a-z0-9]+)*$')

VTAGS = ['ORIGINAL', 'DOCUMENT']

IDS_re = re.compile(r'^\d+(?:,\d+)*$')
PROJ_re = re.compile(r'^proj(?:ect)?:([a-z]+(?:\/[a-z]+)*)$')
VTAG_re = re.compile(r'^(\+|-)([A-Z]+)$')


class Subcommand(object):
    def __init__(self, cmd):
        self.cmd = cmd

    #def config(self, key):
        #if not hasattr(self, '_config'):
            #self._config = read_config_file()
        #return self._config[key]

    def config(self):
        if not hasattr(self, '_config'):
            self._config = read_config_file()
        return self._config


    ################################
    # Terminal interactive methods #
    ################################

    def ask(self, msg, default='yes'):
        while True:
            ans = input('%s (%s) ' % (msg, default))
            if ans == '':
                return True if default == 'yes' else False
            elif ans.lower() in ['y', 'ye', 'yes']:
                return True
            elif ans.lower() in ['n', 'no']:
                return False
            else:
                self.error("Invalid answer")

    # Projects
    #
    def get_or_prompt_project(self, options, default=None):
        if options['no_project']:
            proj = None
        else:
            if options['project']:
                name = options['project']
                self.check_project_name_is_valid(name)
            else:
                if default and self.ask_user('Use project `%s` ?' % default.full_name(), default='yes'):
                    return default
                name = self.prompt_project()

            if not name:
                return None

            if options['project'] and options['create_project']:
                proj, _ = prj.get_or_create_recursively(name)
            else:
                try:
                    proj = prj.get_by_fullname(name)
                except ObjectDoesNotExist:
                    if self.ask('Project `%s` does not exist. Create it ?' % name, default='yes'):
                        proj, _ = prj.get_or_create_recursively(name)
                    else:
                        self.warning_operation_aborted()
        return proj

    def set_project_autocomplete(self):
        completer = self.project_completer()

        # Remove / from delimiter to complete project full_name
        delims = readline.get_completer_delims()
        readline.set_completer_delims(delims.replace('/', ''))

        readline.set_completer(completer.complete)
        readline.parse_and_bind('tab: complete')

    def project_completer(self):
        projs = Project.objects.filter(user_id=1)
        names = [proj.full_name() for proj in projs.all()]
        return AutoCompleter(names)

    def prompt_project(self):
        self.set_project_autocomplete()

        while True:
            name = input('Project: ')
            if not name:
                return None
            elif prj.name_is_valid(name):
                return name
            else:
                self.error_invalid_project_name(name, interactive=True)


    # Notes
    #
    def edit_note_in_editor(self, options, text=None):
        _, f = tempfile.mkstemp()

        # Write notes in tmp
        if text:
            with open(f, 'w') as tmpf:
                tmpf.write(text)

        if options['editor']:
            # @fixme Use custom editor command
            cmd_str = options['editor'].replace('%', f)
            subprocess.call(shlex.split(cmd_str))
        else:
            subprocess.call(['vim', f, '-c', 'startinsert'])  # '-u', 'NONE',

        return f


    ###########################
    # Terminal output methods #
    ###########################

    def success(self, string, interactive=False):
        self.cmd.stdout.write(self.cmd.style.SUCCESS(string))
        if not interactive:
            sys.exit(SUCCESS)

    def warning(self, string, interactive=False):
        self.cmd.stdout.write(self.cmd.style.WARNING(string))
        if not interactive:
            sys.exit(SUCCESS)

    def error(self, string, code, interactive=False):
        self.cmd.stdout.write(self.cmd.style.ERROR(string))
        if not interactive:
            sys.exit(code)

    def not_found(self, string):
        self.error(string, NOT_FOUND)

    def already_exists(self, string):
        self.error(string, EXISTS)

    def invalid(self, string, interactive=False):
        self.error(string, INVALID, interactive)


    def error_no_match(self):
        self.not_found("No match")

    def warning_nothing_to_do(self):
        self.warning("Nothing to do")

    def warning_operation_aborted(self):
        self.warning("Operation aborted")


    # Projects
    #
    def success_project_created(self, project):
        self.success('Created project `%s`' % project.full_name())

    def success_project_deleted(self, proj):
        self.success("Project `%s` deleted" % proj.name)

    def error_project_already_exists(self, name):
        self.already_exists("Project `%s` already exists" % name)

    def error_invalid_project_name(self, name, interactive=False):
        self.invalid("Invalid project name: %s" % name, interactive=False)

    def error_invalid_project_name_or_id(self, name_or_id):
        self.invalid("Invalid project name or id: %s" % name_or_id)

    def error_project_not_found(self, name):
        self.not_found("Project `%s` doesn't exist" % name)


    # Notes
    #
    def success_note_created(self, note):
        s = 'Created note %s' % note.id
        if note.project:
            s += " in %s" % note.project.full_name()
        self.success(s)

    def success_document_modified(self, doc, old_name, desc_mod):
        if old_name:
            if desc_mod:
                s = "Document `%s` renamed to `%s` and modified" % (old_name, doc.name)
            else:
                s = "Document `%s` renamed to `%s`" % (old_name, doc.name)
        else:
            if desc_mod:
                s = "Document `%s` modified" % doc.name
        self.success(s)

    def success_notes_deleted(self, n):
        notes = 'note' if n == 1 else 'notes'
        self.success("%i %s deleted" % (n, notes))

    def error_note_is_not_original(self, note):
        self.invalid("Note `%s` isn't original" % note.id)

    def error_note_not_found(self, note_id):
        self.not_found("Note %s doesn't exist" % note_id)


    # Documents
    #
    def success_document_created(self, doc):
        self.success("Created document `%s`" % doc.name)
        sys.exit(SUCCESS)

    #   success_document_modified

    def success_document_deleted(self, doc):
        self.success("Document `%s` deleted" % doc.name)

    def error_document_already_exists(self, name):
        self.already_exists("The document `%s` already exists" % name)

    def error_invalid_document_name(self, name):
        self.invalid("Invalid document name: %s" % name)

    def error_document_not_found(self, id):
        self.not_found("Document `%s` doesn't exist" % id)

    def error_invalid_document_name_or_id(self, name_or_id):
        self.not_found("Invalid document name or id: %s" % name_or_id)


    # Language
    #
    def success_language_created(self, language):
        self.success('Created language `%s`' % language.code)

    def error_invalid_language_code(self, code, interactive=False):
        self.invalid("Invalid language code: %s" % code, interactive=False)

    def error_language_already_exists(self, code):
        self.already_exists("Language `%s` already exists" % code)

    def error_language_does_not_exist(self, code):
        self.not_found("Language `%s` does not exists" % code)


    # LexicalUnit
    #
    def error_lemma_already_exists(self, unit):
        self.already_exists("Lemma `%s` already exists in language `%s`" % (unit.lemma, unit.language))

    def success_lexical_unit_created(self, unit):
        self.success('Created lexical unit `%i` in language `%s`' % (unit.id, unit.language.code))

    def success_lexical_unit_modified(self, unit):
        self.success('Modified lexical unit `%i`' % unit.id)

    def success_lexical_unit_deleted(self, id):
        self.success('Deleted lexical unit `%i`' % id)

    def error_lexical_entry_not_found(self, id):
        self.not_found("Lexical unit `%i` does not exists" % id)

    def success_lexical_pattern_created(self, pat):
        self.success('Created lexical pattern `%i` for entry `%s`' % (pat.id, pat.lexical_unit.lemma))

    def error_lexical_pattern_not_found(self, pat_id):
        self.not_found("Lexical pattern `%i` does not exists" % pat_id)

    def success_lexical_pattern_modified(self, pat):
        self.success('Modified lexical pattern `%i`' % pat.id)

    def success_lexical_pattern_deleted(self, pat_id):
        self.success('Deleted lexical pattern `%i`' % pat_id)

    def error_lexical_pattern_already_exists(self, desc):
        self.already_exists("Lexical pattern already exists: %s" % desc)


    ###############################
    # Find models or return error #
    ###############################

    def find_project_by_name_or_id_or_error(self, name_or_id):
        try:
            return prj.get_by_fullname_or_id(name_or_id)
        except ValueError as e:
            self.error_invalid_project_name_or_id(name_or_id)
        except ObjectDoesNotExist as e:
            self.error_project_not_found(name_or_id)

    def find_note_by_id_or_error(self, note_id):
        try:
            return Note.objects.get(id=note_id)
        except:
            self.error_note_not_found(note_id)

    def find_document_by_id_or_error(self, doc_id):
        try:
            return Document.objects.get(id=doc_id)
        except:
            self.error_document_not_found(doc_id)

    def find_document_by_name_or_error(self, name):
        try:
            return Document.objects.get(name=name)
        except:
            self.error_document_not_found(name)

    def find_document_by_name_or_id_or_error(self, name_or_id):
        name_or_id = str(name_or_id)
        if re.match(r'^[0-9]+$', name_or_id):
            q = {'id': int(name_or_id)}
        elif DOCNAME_re.match(str(name_or_id)):
            q = {'name': name_or_id}
        else:
            self.error_invalid_document_name_or_id(name_or_id)

        try:
            return Document.objects.get(**q)
        except:
            self.error_document_not_found(name_or_id)


    #####################
    # Validation Guards #
    #####################

    def check_project_name_is_valid(self, name):
        if not prj.name_is_valid(name):
            self.error_invalid_project_name(name)

    def check_note_is_original(self, note):
        if not note.original:
            self.error_note_is_not_original(note)

    def check_document_name_is_valid(self, name):
        if not DOCNAME_re.match(name):
            self.error_invalid_document_name(name)

    def check_document_name_does_not_exist(self, name):
        try:
            # @fixme Direct use of the model object
            Document.objects.get(user_id=1, name=name)
        except:
            return
        self.error_document_already_exists(name)

    def check_language_code_is_valid(self, code):
        if not lang.code_is_valid(code):
            self.error_invalid_language_code(code)

    def check_language_exists(self, code):
        if not Language.objects.filter(code=code).count():
            self.error_language_does_not_exist(code)

    def check_language_does_not_exist(self, code):
        if Language.objects.filter(code=code).count():
            self.error_language_already_exists(code)

    def check_lemma_does_not_exist(self, lang, lemma):
        q = LexicalUnit.objects.filter(language=lang, lemma=lemma)
        if q.count():
            self.error_lemma_already_exists(q.first())


    def filter_notes(self, filters):
        q = self.filter_query(filters)
        return Note.objects.filter(**q)

    # @todo Move to _functions.py
    #
    def filter_query(self, filters):
        ids, proj_name, vtags = set(), None, {}

        for f in filters:
            if IDS_re.match(f):
                ids.update(int(i) for i in f.split(','))
                continue

            m = PROJ_re.match(f)
            if m:
                proj_name = m.group(1)
                continue

            m = VTAG_re.match(f)
            if m:
                sign, vtag = m.group(1), m.group(2)
                if vtag in VTAGS:
                    vtags[vtag] = True if sign == '+' else False
                else:
                    self.cmd.stderr.write(self.cmd.style.ERROR("Unknown virtual tag `%s`" % vtag))
                    exit(1)

        q = {}
        if ids: q['id__in'] = list(ids)

        if proj_name:
            #proj = prj.get_project(proj_name)
            proj = prj.get_by_fullname(proj_name)
            if proj:
                q['project'] = proj
            else:
                self.cmd.stderr.write(self.cmd.style.ERROR("Unknown project `%s`" % proj_name))
                exit(1)

        if 'ORIGINAL' in vtags:
            q['original'] = vtags['ORIGINAL']

        if 'DOCUMENT' in vtags:
            q['documents__isnull'] = not vtags['DOCUMENT']

        return q


    # @fixme This is a helper
    #
    def create_document(self, name, note, desc=None):
        doc = Document(user_id=1, name=name, note=note, description=desc)
        doc.save()
        return doc


class AutoCompleter(object):
    def __init__(self, options):
        self.options = sorted(options)

    def complete(self, text, state):
        if state == 0:  # on first trigger, build possible matches
            if text:  # cache matches (entries that start with entered text)
                self.matches = [s for s in self.options
                                  if s and s.startswith(text)]
            else:  # no text entered, all matches possible
                self.matches = self.options[:]

        # return match indexed by state
        try:
            return self.matches[state]
        except IndexError:
            return None


