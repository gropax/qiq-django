from core.cli.command import Command, command
from lexical_units.cli.utils import Utils
from lexical_units.cli.commands.pattern.pattern import PatternCommand
from lexical_units.models import LexicalUnit, LexicalPattern
from languages.models import Language
import lexical_units.utils as lex


@command('new', PatternCommand)
class NewCommand(Command, Utils):
    def add_arguments(self, parser):
        parser.add_argument('lang', type=str, help='the iso-3 language code (ex: fra)')
        parser.add_argument('pattern', type=str, help='the pattern description')
        parser.add_argument('-l', '--lemma', type=str,
                            help='use given lemma instead of guessing it')
        parser.add_argument('-f', '--force-lemma', action='store_true', default=False,
                            help='create lemma if it does not exist')

    def action(self, args):
        lang = args.lang
        self.check_language_code_is_valid(lang)
        self.check_language_exists(lang)

        cfg = self.config()
        language = Language.objects.get(code=lang)
        lang_cfg = cfg.get('languages').get(lang, {})

        desc = args.pattern
        self.check_lexical_pattern_does_not_exist(desc, lang_cfg)

        pat = lex.parse_pattern(desc)

        if args.lemma:
            lemma = args.lemma
        else:
            lemma = pat.lexical_unit(lang_cfg)

        q = LexicalUnit.objects.filter(user_id=1, language=language, lemma=lemma)
        if q.count():
            unit = q.first()
        else:
            if args.force_lemma or \
              self.ask("Lexical unit `%s` doesn't exist. Create it ?" % lemma, default='yes'):
                unit = LexicalUnit(user_id=1, language=language, lemma=lemma)
                unit.save()
            else:
                self.warning_nothing_to_do()

        lexpat = LexicalPattern(lexical_unit=unit, description=args.pattern)
        lexpat.save()

        self.success_lexical_pattern_created(lexpat)

    def check_lexical_pattern_does_not_exist(self, desc, cfg):
        pat = lex.parse_pattern(desc)
        q = LexicalPattern.objects.filter(lexical_unit__lemma=pat.lexical_unit(cfg),
                                          lexical_unit__user_id=1,
                                          description=desc)
        if q.count():
            self.error_lexical_pattern_already_exists(desc)
