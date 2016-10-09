from qiq.test import TestCase
from django.contrib.auth.models import User
from languages.models import Language
from lexical_units.models import LexicalUnit, LexicalPattern


class NewCommand(TestCase):
    def test_created(self):
        self.assert_success('language', 'new', 'fra', 'French')
        self.assert_success('lexical', 'unit', 'new', 'fra', 'manger')

    def test_error_invalid_code(self):
        self.assert_success('language', 'new', 'fra', 'French')
        self.assert_invalid('lexical', 'unit', 'new', 'fr', 'manger')

    def test_error_language_not_found(self):
        self.assert_not_found('lexical', 'unit', 'new', 'fra', 'French')


class ListCommand(TestCase):
    def test_success(self):
        self.assert_success('language', 'new', 'fra', 'French')
        self.assert_success('lexical', 'unit', 'new', 'fra', 'manger')
        self.assert_success('lexical', 'unit', 'list', 'fra')

    def test_error_no_match(self):
        self.assert_success('language', 'new', 'fra', 'French')
        self.assert_not_found('lexical', 'unit', 'list', 'fra')

    def test_error_invalid_code(self):
        self.assert_success('language', 'new', 'fra', 'French')
        self.assert_invalid('lexical', 'unit', 'new', 'fr', 'manger')

    def test_error_language_not_found(self):
        self.assert_not_found('lexical', 'unit', 'new', 'fra', 'French')


class DeleteCommand(TestCase):
    def test_success(self):
        lang = Language(code='fra', name='French'); lang.save()
        unit = LexicalUnit(user_id=1, language=lang, lemma='manger'); unit.save()
        self.assert_success('lexical', 'unit', 'delete', unit.id)

    def test_error_lexical_unit_not_found(self):
        self.assert_not_found('lexical', 'unit', 'delete', 123)


class ModifyCommand(TestCase):
    def test_success(self):
        lang = Language(code='fra', name='French'); lang.save()
        unit = LexicalUnit(user_id=1, language=lang, lemma='manger'); unit.save()
        self.assert_success('lexical', 'unit', 'modify', unit.id, '-l', 'manger')

    def test_error_lexical_unit_not_found(self):
        self.assert_not_found('lexical', 'unit', 'delete', 123)


class InfoCommand(TestCase):
    def test_success(self):
        User(id=1, username='maxime').save()
        lang = Language(code='fra', name='French'); lang.save()
        unit = LexicalUnit(user_id=1, language=lang, lemma='donner'); unit.save()
        pat  = LexicalPattern(lexical_unit=unit, description='X *donner* Y'); pat.save()
        pat  = LexicalPattern(lexical_unit=unit, description='X *donner* Y à Z_hum'); pat.save()
        self.assert_success('lexical', 'unit', 'info', unit.id)

    def test_error_not_found(self):
        self.assert_not_found('lexical', 'unit', 'info', 123)
