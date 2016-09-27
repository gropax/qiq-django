from cli.management.commands._subcommand import Subcommand
from lexical_units.models import LexicalUnit, LexicalPattern
from languages.models import Language
import lexical_units.utils as lex


class NewCommand(Subcommand):
    def add_arguments(self, parser):
        parser.add_argument('lang', type=str, help='the iso-3 language code (ex: fra)')
        parser.add_argument('pattern', type=str, help='the pattern description')

    def execute(self, args, options):
        lang = options['lang']
        self.check_language_code_is_valid(lang)
        self.check_language_exists(lang)

        cfg = self.config()

        language = Language.objects.get(code=lang)
        lang_cfg = cfg.get('languages').get(lang)

        pat = lex.parse_pattern(options['pattern'])
        lemma = pat.lexical_unit(lang_cfg)

        q = LexicalUnit.objects.filter(user_id=1, language=language, lemma=lemma)
        if q.count():
            unit = q.first()
        else:
            if self.ask("Lexical unit `%s` doesn't exist. Create it ?" % lemma, default='yes'):
                unit = LexicalUnit(user_id=1, language=language, lemma=lemma)
                unit.save()
            else:
                self.warning_nothing_to_do()

        lexpat = LexicalPattern(lexical_unit=unit, description=options['pattern'])
        lexpat.save()

        self.success_lexical_pattern_created(lexpat)
