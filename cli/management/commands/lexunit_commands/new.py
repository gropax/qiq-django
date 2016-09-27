from cli.management.commands._subcommand import Subcommand
from languages.models import Language
from lexical_units.models import LexicalUnit


class NewCommand(Subcommand):
    def add_arguments(self, parser):
        parser.add_argument('language', type=str, help='the iso-3 of the language')
        parser.add_argument('lemma', type=str, help='the lemma of the lexical unit')

    def execute(self, args, options):
        lang = options['language']
        self.check_language_code_is_valid(lang)
        self.check_language_exists(lang)

        lemma = options['lemma']
        self.check_lemma_does_not_exist(lang, lemma)  # @fixme Multiple entries for one lemma ??

        language = Language.objects.get(code=lang)
        unit = LexicalUnit(user_id=1, language_id=lang, lemma=lemma)
        unit.save()

        self.success_lexical_unit_created(unit)
