from core.cli.command import Command, command
from lexical_units.cli.utils import Utils
from lexical_units.cli.commands.unit.unit import UnitCommand
from languages.models import Language
from lexical_units.models import LexicalUnit


@command('new', UnitCommand)
class NewCommand(Command, Utils):
    def add_arguments(self, parser):
        parser.add_argument('language', type=str, help='the iso-3 of the language')
        parser.add_argument('lemma', type=str, help='the lemma of the lexical unit')
        parser.add_argument('-c', '--category', type=str, choices=LexicalUnit.CATEGORIES,
                            metavar='CAT', help='the grammatical category of the lexical unit')

    def action(self, args):
        lang = args.language
        self.check_language_code_is_valid(lang)
        self.check_language_exists(lang)

        lemma = args.lemma
        self.check_lemma_does_not_exist(lang, lemma)  # @fixme Multiple entries for one lemma ??

        language = Language.objects.get(code=lang)
        unit = LexicalUnit(user_id=1, language_id=lang, lemma=lemma)

        if args.category:
            unit.grammatical_category = args.category

        unit.save()

        self.success_lexical_unit_created(unit)
