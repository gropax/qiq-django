import sys
import re
from notes.models import Note
from notes.helpers import virtual_tags
from qiq.common import SUCCESS, INVALID, EXISTS, NOT_FOUND
from termblocks import TableBlock


class Subcommand(object):
    def __init__(self, cmd):
        self.cmd = cmd


    ###########################
    # Terminal output methods #
    ###########################

    def success(self, string):
        self.cmd.stdout.write(self.cmd.style.SUCCESS(string))

    def error(self, string):
        self.cmd.stdout.write(self.cmd.style.ERROR(string))

    def warning(self, string):
        self.cmd.stdout.write(self.cmd.style.WARNING(string))


    def error_no_match(self):
        self.error("No match")
        sys.exit(NOT_FOUND)

    def warning_nothing_to_do(self):
        self.warning("Nothing to do")
        sys.exit(SUCCESS)

    def error_note_not_found(self, note_id):
        self.error("Note %s doesn't exist" % note_id)
        sys.exit(NOT_FOUND)

    def error_invalid_project_name(self, name, interactive=False):
        self.error("Invalid project name: %s" % name)
        if not interactive:
            sys.exit(INVALID)


    ###############################
    # Find models or return error #
    ###############################

    def find_note_by_id_or_error(self, note_id):
        try:
            return Note.objects.get(id=note_id)
        except:
            self.error_note_not_found(note_id)


    #######################
    # Terminal Formatting #
    #######################

    def headers_data(self, headers):
        options = {'style': ['bold', 'underline']}

        cells = []
        for h in headers:
            cells.append(self.cell_data(h))

        return {'cells': cells, 'options': options}

    def format_table(self, rows):
        # Add odd line coloring
        for i, row in enumerate(rows):
            if not i % 2:
                row['options']['background'] = 'grey'

        options = {
            'max_row_height': 1,
            'column_separator': ' ',
        }
        return TableBlock({'rows': rows, 'options': options})

    def model_table(self, data):
        headers = ['Name', 'Value']

        rows = [self.headers_data(headers)]
        for label, value in data:
            rows.append(self.model_row_data(label, value))

        return self.format_table(rows)

    def model_row_data(self, label, value):
        cells = [self.cell_data(label)]
        cells.append(self.format_cell(value))
        return {'cells': cells, 'options': {}}

    def list_table(self, headers, models, format_proc):
        rows = [self.headers_data(headers)]
        for model in models:
            vals = format_proc(model)
            cells = [self.format_cell(v) for v in vals]
            options = {}
            rows.append({'cells': cells, 'options': options})

        return self.format_table(rows)

    def format_cell(self, value):
        if type(value) is list:
            val, opts = value
        else:
            val, opts = value, {}
        return self.cell_data(val, opts)

    def cell_data(self, text, options={}):
        cell = {'text': str(text)}
        if options: cell['options'] = options
        return cell


    def format_text(self, note):
        return re.sub(r'\n+', '  ', note.text)

    def format_original(self, note):
        orig = note.original
        str = '✓' if orig else '✗'
        color = 'green' if orig else 'red'
        return [str, {'color': color}]

    def format_project_name(self, proj):
        return proj.full_name() if proj else '-'

    def format_document_list(self, note):
        return ", ".join(d.name for d in note.documents.all()) or '-'

    def format_references(self, refs):
        return ",".join(str(n.id) for n in refs.all()) or '-'

    def format_virtual_tags(self, note):
        return " ".join(tag for tag in virtual_tags(note))

    def format_creation_date(self, note):
        return note.created.strftime("%Y-%m-%d %H:%M:%S") + " (%s)" % note.age() #self.note_age(note)

    def format_project_description(self, proj):
        return proj.description or '-'

    def format_document_title(self, doc):
        return doc.description or '-'
