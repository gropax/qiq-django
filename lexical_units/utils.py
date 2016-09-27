import re
from termcolor import colored


class Pattern(object):
    def __init__(self, items):
        self.items = items

    def format_termblock(self, opts={}):
        return [i.format_termblock(opts) for i in self.items]

    def format(self, opts={}):
        return ''.join(i.format(opts) for i in self.items)

    def lexical_unit(self, opts):
        sep = opts.get('separator', '')
        return sep.join(i.text for i in self.items
                               if i.__class__ == LexicalUnit)

    def __str__(self):
        return "".join(i.__str__() for i in self.items)

class LexicalUnit(object):
    def __init__(self, text):
        self.text = text

    def format_termblock(self, opts={}):
        lex_opts = opts.get('lexical_units', {})
        fg = lex_opts.get('fgcolor', None)
        bg = lex_opts.get('bgcolor', None)
        style = lex_opts.get('style', [])

        options = {'color': fg, 'background': bg, 'style': style}

        return {'text': self.text, 'options': options}

    def format(self, opts={}):
        lex_opts = opts.get('lexical_units', {})
        fg = lex_opts.get('fgcolor', None)
        bg = lex_opts.get('bgcolor', None)
        bg = bg and 'on_' + bg
        style = lex_opts.get('style', [])

        if fg or bg or style:
            return colored(self.text, fg, bg, attrs=style)
        else:
            return self.text

    def __str__(self):
        return '*%s*' % self.text

class SynArg(object):
    def __init__(self, text, traits):
        self.text = text
        self.traits = traits

    def format_termblock(self, opts={}):
        traits_opts = opts.get('traits', {})
        display_traits = list(self.traits)

        t = next(t for t in self.traits if t in traits_opts)
        if t:
            t_opt = traits_opts.get(t)
            fg = t_opt.get('fgcolor', None)
            bg = t_opt.get('bgcolor', None)
            bg = bg and 'on_' + bg
            style = t_opt.get('style', [])

            if not t_opt.get('keep', False):
                display_traits.remove(t)
        else:
            fg, bg, style = None, None, []

        options = {'color': fg, 'background': bg, 'style': style}

        txt = self.text
        if len(display_traits) > 0 and ' ' in txt:
            txt = "[%s]" % txt

        arg = txt + ''.join("_" + t for t in display_traits)

        return {'text': arg, 'options': options}

    def format(self, opts={}):
        traits_opts = opts.get('traits', {})

        display_traits = list(self.traits)

        t = next(t for t in self.traits if t in traits_opts)

        if t:
            t_opt = traits_opts.get(t)
            fg = t_opt.get('fgcolor', None)
            bg = t_opt.get('bgcolor', None)
            bg = bg and 'on_' + bg
            style = t_opt.get('style', [])

            if not t_opt.get('keep', False):
                display_traits.remove(t)
        else:
            fg, bg, style = None, None, []

        txt = self.text
        if len(display_traits) > 0 and ' ' in txt:
            txt = "[%s]" % txt

        arg = txt + ''.join("_" + t for t in display_traits)

        if fg or bg or style:
            return colored(arg, fg, bg, attrs=style)
        else:
            return arg

    def __str__(self):
        text = "[%s]" % self.text if ' ' in self.text else self.text
        traits_str = ''.join('_' + t for t in self.traits)
        return text + traits_str

class Text(object):
    def __init__(self, text):
        self.text = text

    def format_termblock(self, opts={}):
        return {'text': self.text, 'options': {}}

    def format(self, opts={}):
        return self.text

    def __str__(self):
        return self.text


MARKUP_re = re.compile(r'((?:(?:[\w]+|\[[\s\w]+\])(?:_[a-zA-z0-9]+)+)|(?:\*[\s\w]+\*))')
LEMMA_re = re.compile(r'\*([\s\w]+)\*')
SYNARG_re = re.compile(r'\[?([^_\]]*)\]?(_[a-zA-z0-9]+)+')

def parse_pattern(pat):
    matches = list(MARKUP_re.finditer(pat))
    items = []
    cur = 0
    for m in matches:
        if m.start() > cur:
            items.append(Text(pat[cur:m.start()]))

        m_lemma = LEMMA_re.match(m.group(0))
        if m_lemma:
            items.append(LexicalUnit(m_lemma.group(1)))

        m_synarg = SYNARG_re.match(m.group(0))
        if m_synarg:
            text, *traits_s = m_synarg.groups()
            traits = traits_s[0][1:].split('_')
            items.append(SynArg(text, traits))

        cur = m.end()

    return Pattern(items)



if __name__ == '__main__':
    #ret = parse_pattern('φασδφ_nom_sg *donner* [ασδφ nrst]_acc_3 *bougle* à Z_dat_2')
    ret = parse_pattern('X_nom *donner* Y_acc à Z_dat')
    print(ret.format({
        'lexical_item': {'style': ['underline']},
        'traits': {
            'nom': {'keep': False, 'fgcolor': 'green', 'style': ['bold']},
            'acc': {'keep': False, 'fgcolor': 'blue', 'style': ['bold']},
            'dat': {'keep': False, 'fgcolor': 'red', 'style': ['bold']},
        }
    }))
    #print(ret.lexical_item())
