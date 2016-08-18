import os
from termcolor import colored
from textwrap import TextWrapper


class Block(object):
    def __init__(self, **options):
        self.options = options
        self.parent = options.get('parent')

    def width(self):
        if not hasattr(self, '_width'):
            self._width = self.parent.child_width(self) if self.parent else self.tty_width()
        return self._width

    def tty_width(self):
        rows, cols = os.popen('stty size', 'r').read().split()
        return int(cols)

    def child_width(self, block):
        return self.width()

    def format(self):
        return "\n".join(self.formated_lines())


class VerticalLayout(Block):
    def __init__(self, blocks, **options):
        super(VerticalLayout, self).__init__(**options)
        self.blocks = blocks

    def formated_lines(self):
        return sum((blk.formated_lines() for blk in self.blocks), [])


class TextBlock(Block):
    def __init__(self, text, **options):
        super(TextBlock, self).__init__(**options)
        self.text = text

    def formated_lines(self):
        wrapper = TextWrapper(width=self.width())
        return wrapper.wrap(self.text)


FILLING_CHAR = ' '

class MarginBlock(Block):
    def __init__(self, block, **options):
        super(MarginBlock, self).__init__(**options)

        self.child = block
        block.parent = self

        self.margin = {
            'left': options.get('left', 0),
            'right': options.get('right', 0),
            'top': options.get('top', 0),
            'bottom': options.get('bottom', 0),
        }

    def child_width(self, block):
        width = self.width() - self.margin['left'] - self.margin['right']
        return max(width, 0)

    def formated_lines(self):
        top = [FILLING_CHAR * self.width()] * self.margin['top']
        bottom = [FILLING_CHAR * self.width()] * self.margin['bottom']
        middle = [FILLING_CHAR * self.margin['left'] + line +
                  FILLING_CHAR * self.margin['right'] for line in self.child.formated_lines()]
        return top + middle + bottom


COL_SEPARATOR = ' '

class TableBlock(Block):
    def __init__(self, data, **options):
        super(TableBlock, self).__init__(**options)
        self.data = [[str(cell) for cell in line] for line in data]
        self.colnos = self.columns_number(data)

    def formated_lines(self):
        col_len = self.columns_length(self.data)
        tot_w = sum(col_len) + (self.colnos - 1) * len(COL_SEPARATOR)
        tab_w = self.width()
        max_line = self.options.get('max_line', 0)

        if tot_w > tab_w:
            widest, max_l = None, 0
            for i, l in enumerate(col_len):
                if l >= max_l:
                    max_l, widest = l, i

            new_l = max_l + tab_w - tot_w
            col_len[widest] = new_l
            wrapper = TextWrapper(width=new_l)

            rows = []
            for row in self.data:
                widest_cell = row[widest]
                wrapped = wrapper.wrap(widest_cell)

                if max_line and len(wrapped) > max_line:
                    wrapped = wrapped[:max_line-1] + [self.add_suspension_dots(wrapped[max_line-1], new_l)]

                lineno = len(wrapped)

                lines = []
                for i in range(lineno):
                    line = []
                    for j, cell in enumerate(row):
                        if j == widest:
                            line.append(wrapped[i].ljust(new_l))
                        else:
                            cell_line = cell if i == 0 else ''
                            line.append(cell_line.ljust(col_len[j]))
                    lines.append(line)

                rows.append(lines)
        else:
            # Widen the right-most column to fill the available width
            if tot_w < tab_w:
                col_len[-1] = col_len[-1] + tab_w - tot_w

            rows = []
            for row in self.data:
                line = []
                for i, cell in enumerate(row):
                    line.append(cell.ljust(col_len[i]))
                rows.append([line])

        headers = self.options.get('headers')
        if headers:
            rows[0] = [[colored(cell_line, attrs=headers) for cell_line in lines] for lines in rows[0]]

        formated_rows = ["".join(COL_SEPARATOR.join(cell_line for cell_line in line)
                            for line in row) for row in rows]

        color_line = self.options.get('color_line')
        if color_line:
            color = "on_%s" % color_line
            colored_rows = []
            for i, row in enumerate(formated_rows):
                if i % 2:
                    colored_rows.append(colored(row, None, color))
                else:
                    colored_rows.append(row)
            formated_rows = colored_rows

        return "\n".join(formated_rows).split('\n')  # @fixme ugly

    def columns_length(self, data):
        col_len = [0] * self.colnos
        for line in self.data:
            for i, cell in enumerate(line):
                if len(cell) > col_len[i]:
                    col_len[i] = len(cell)
        return col_len

    def columns_number(self, data):
        return len(data[1])

    def add_suspension_dots(self, line, l):
        just = line.ljust(l)
        space, i = True, 0
        for j in reversed(range(l)):
            if space:
                if just[j] == ' ':
                    i += 1
                else:
                    if i >= 3:
                        break
                    else:
                        space = False
            else:
                i += 1
                if just[j] == ' ':
                    space = True

        newline = just[0:l-i] + '...' + ' ' * (i - 3)

        return newline
