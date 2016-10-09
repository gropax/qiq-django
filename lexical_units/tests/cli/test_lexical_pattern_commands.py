from qiq.test import TestCase
from qiq.common import SUCCESS, INVALID, EXISTS, NOT_FOUND
from django.contrib.auth.models import User
from languages.models import Language
from lexical_units.models import LexicalUnit, LexicalPattern


class NewCommand(TestCase):
    def test_created_in_existing_lexical_unit(self):
        lang = Language(code='fra', name='French'); lang.save()
        unit = LexicalUnit(user_id=1, language=lang, lemma='donner'); unit.save()
        self.assert_success('lexical', 'pattern', 'new', 'fra', 'X *donner* Y à Z_hum')

    def test_created_with_lexical_unit(self):
        lang = Language(code='fra', name='French'); lang.save()
        self.assert_success('lexical', 'pattern', 'new', 'fra', 'X *donner* Y à Z_hum', '--force-lemma')

    def test_created_specifying_lexical_unit(self):
        lang = Language(code='fra', name='French'); lang.save()
        unit = LexicalUnit(user_id=1, language=lang, lemma='manger'); unit.save()
        self.assert_success('lexical', 'pattern', 'new', 'fra', 'X *donner* Y à Z_hum', '-l', 'manger')

    def test_error_already_exist(self):
        User(id=1, username='maxime').save()
        lang = Language(code='fra', name='French'); lang.save()
        self.assert_success('lexical', 'pattern', 'new', 'fra', 'X *donner* Y à Z_hum', '--force-lemma')
        self.assert_exists('lexical', 'pattern', 'new', 'fra', 'X *donner* Y à Z_hum', '--force-lemma')


class ListCommand(TestCase):
    def test_success(self):
        self.assert_success('language', 'new', 'fra', 'French')
        self.assert_success('lexical', 'pattern', 'new', 'fra', 'X *donner* Y à Z_hum', '--force-lemma')
        self.assert_success('lexical', 'pattern', 'list', 'fra')

    def test_error_no_match(self):
        self.assert_success('language', 'new', 'fra', 'French')
        self.assert_not_found('lexical', 'pattern', 'list', 'fra')

    def test_error_invalid_code(self):
        self.assert_success('language', 'new', 'fra', 'French')
        self.assert_invalid('lexical', 'pattern', 'new', 'fr', 'X *donner* Y à Z_hum', '--force-lemma')

    def test_error_language_not_found(self):
        self.assert_not_found('lexical', 'pattern', 'new', 'fra', 'X *donner* Y à Z_hum', '--force-lemma')


class DeleteCommand(TestCase):
    def test_success(self):
        lang = Language(code='fra', name='French'); lang.save()
        unit = LexicalUnit(user_id=1, language=lang, lemma='donner'); unit.save()
        pat  = LexicalPattern(lexical_unit=unit, description='X *donner* Y à Z_hum'); pat.save()
        self.assert_success('lexical', 'pattern', 'delete', pat.id)

    def test_error_lexical_unit_not_found(self):
        self.assert_not_found('lexical', 'pattern', 'delete', 123)


class ModifyCommand(TestCase):
    def test_success(self):
        lang = Language(code='fra', name='French'); lang.save()
        unit = LexicalUnit(user_id=1, language=lang, lemma='donner'); unit.save()
        pat  = LexicalPattern(lexical_unit=unit, description='X *donner* Y'); pat.save()
        self.assert_success('lexical', 'pattern', 'modify', pat.id, '-d', 'X *donner* Y à Z_hum')

    def test_error_lexical_unit_not_found(self):
        self.assert_not_found('lexical', 'pattern', 'delete', 123)


class InfoCommand(TestCase):
    def test_success(self):
        User(id=1, username='maxime').save()
        lang = Language(code='fra', name='French'); lang.save()
        unit = LexicalUnit(user_id=1, language=lang, lemma='donner'); unit.save()
        pat  = LexicalPattern(lexical_unit=unit, description='X *donner* Y'); pat.save()
        self.assert_success('lexical', 'pattern', 'info', pat.id)

    def test_error_not_found(self):
        self.assert_not_found('lexical', 'pattern', 'info', 123)
