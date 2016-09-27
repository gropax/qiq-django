import re
from termblocks import TableBlock
from notes.helpers import virtual_tags


def headers_data(headers):
    options = {'style': ['bold', 'underline']}

    cells = []
    for h in headers:
        cells.append(cell_data(h))

    return {'cells': cells, 'options': options}

def format_table(rows):
    # Add odd line coloring
    for i, row in enumerate(rows):
        if not i % 2:
            row['options']['background'] = 'grey'

    options = {
        'max_row_height': 1,
        'column_separator': ' ',
    }
    return TableBlock({'rows': rows, 'options': options})

def model_table(data):
    headers = ['Name', 'Value']

    rows = [headers_data(headers)]
    for label, value in data:
        rows.append(model_row_data(label, value))

    return format_table(rows)

def model_row_data(label, value):
    cells = [cell_data(label)]
    cells.append(format_cell(value))
    return {'cells': cells, 'options': {}}

def list_table(headers, models, format_proc):
    rows = [headers_data(headers)]
    for model in models:
        vals = format_proc(model)
        cells = [format_cell(v) for v in vals]
        options = {}
        rows.append({'cells': cells, 'options': options})

    return format_table(rows)

def format_cell(value):
    if type(value) is list:
        fst = value[0]
        if isinstance(fst, dict):
            val, opts = value, {}
        else:
            val, opts = str(value[0]), value[1]
    else:
        val, opts = str(value), {}
    return cell_data(val, opts)

def cell_data(text, options={}):
    cell = {'text': text}
    if options: cell['options'] = options
    return cell


def format_text(note):
    return re.sub(r'\n+', '  ', note.text)

def format_original(note):
    orig = note.original
    str = '✓' if orig else '✗'
    color = 'green' if orig else 'red'
    return [str, {'color': color}]

def format_project_name(proj):
    return proj.full_name() if proj else '-'

def format_document_list(note):
    return ", ".join(d.name for d in note.documents.all()) or '-'

def format_references(refs):
    return ",".join(str(n.id) for n in refs.all()) or '-'

def format_virtual_tags(note):
    return " ".join(tag for tag in virtual_tags(note))

def format_creation_date(note):
    return note.created.strftime("%Y-%m-%d %H:%M:%S") + " (%s)" % note.age() #note_age(note)

def format_project_description(proj):
    return proj.description or '-'

def format_document_title(doc):
    return doc.description or '-'

def format_project_note_no(n):
    color = None
    if n <= 0:
        color = 'grey'
    elif n == 1:
        color = 'cyan'
    elif n <= 5:
        color = 'green'
    elif n <= 10:
        color = 'yellow'
    else:
        color = 'red'

    return [str(n), {'color': color, 'style': ['bold']}]
