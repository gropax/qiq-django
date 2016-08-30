import re
import subprocess
import tempfile
import readline  # Used for autocomplete
from notes.models import Note
from projects.models import Project
from projects.helpers import parse_project_name, get_project, get_or_create_project, project_name_is_valid
from cli.management.commands._subcommand import Subcommand


VTAGS = ['ORIGINAL', 'DOCUMENT']

IDS_re = re.compile(r'^\d+(?:,\d+)*$')
PROJ_re = re.compile(r'^proj(?:ect)?:([a-z]+(?:\.[a-z]+)*)$')
VTAG_re = re.compile(r'^(\+|-)([A-Z]+)$')


class NoteCommand(Subcommand):

    ###########################
    # Terminal output methods #
    ###########################

    def success_note_created(self, note):
        s = 'Created note %s' % note.id
        if note.project:
            s += " in %s" % note.project.full_name()
        self.cmd.stdout.write(self.cmd.style.SUCCESS(s))

    def success_notes_deleted(self, n):
        notes = 'note' if n == 1 else 'notes'
        self.success("%i %s deleted" % (n, notes))


    ################
    # Text Edition #
    ################

    def edit_note_in_editor(self, options, text=None):
        _, f = tempfile.mkstemp()

        # Write notes in tmp
        if text:
            with open(f, 'w') as tmpf:
                tmpf.write(text)

        subprocess.call(['vim', f, '-c', 'startinsert'])  # '-u', 'NONE',

        # @fixme Use custom editor command
        #cmd = options['editor'].replace('%', f)
        #subprocess.call(cmd)

        return f


    ########################
    # Interactive Commands #
    ########################

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
            elif project_name_is_valid(name):
                return name
            else:
                self.error_invalid_project_name(name, interactive=True)

    def ask_user(self, msg, default='yes'):
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

    def get_or_prompt_project(self, options, default=None):
        if options['no_project']:
            proj = None
        else:
            if options['project']:
                name = options['project']
                self.check_project_name_is_valid(name)
            else:
                if default and self.ask_user('Use project `%s` ?' % default.name, default='yes'):
                    return default
                name = self.prompt_project()

            if options['project'] and options['create_project']:
                proj, _ = get_or_create_project(name)
            else:
                proj = get_project(name)
                if not proj:
                    if self.ask_user('Create it ?', default='yes'):
                        proj, _ = get_or_create_project(name)
                    else:
                        exit(1)
        return proj

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
            proj = get_project(proj_name)
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
