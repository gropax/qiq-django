from languages.cli.utils import Utils as Base
from lexical_units.models import LexicalUnit, LexicalPattern


class Utils(Base):
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

    def check_lemma_does_not_exist(self, lang, lemma):
        q = LexicalUnit.objects.filter(language=lang, lemma=lemma)
        if q.count():
            self.error_lemma_already_exists(q.first())

