from qiq.test import TestCase
from qiq.common import SUCCESS, INVALID, EXISTS, NOT_FOUND
from django.contrib.auth.models import User
from languages.models import Language
from lexical_units.models import LexicalUnit, LexicalPattern


class NewCommand(TestCase):
    def test_created_in_existing_lexical_unit(self):
        lang = Language(code='fra', name='French'); lang.save()
        unit = LexicalUnit(user_id=1, language=lang, lemma='donner'); unit.save()
        self.assert_status(SUCCESS, 'lexpat', 'new', 'fra', 'X *donner* Y à Z_hum')

    def test_created_with_lexical_unit(self):
        lang = Language(code='fra', name='French'); lang.save()
        self.assert_status(SUCCESS, 'lexpat', 'new', 'fra', 'X *donner* Y à Z_hum', '--force-lemma')

    def test_error_already_exist(self):
        User(id=1, username='maxime').save()
        lang = Language(code='fra', name='French'); lang.save()
        self.assert_status(SUCCESS, 'lexpat', 'new', 'fra', 'X *donner* Y à Z_hum', '--force-lemma')
        self.assert_status(EXISTS, 'lexpat', 'new', 'fra', 'X *donner* Y à Z_hum', '--force-lemma')


class ListCommand(TestCase):
    def test_success(self):
        self.assert_status(SUCCESS, 'language', 'new', 'fra', 'French')
        self.assert_status(SUCCESS, 'lexpat', 'new', 'fra', 'X *donner* Y à Z_hum', '--force-lemma')
        self.assert_status(SUCCESS, 'lexpat', 'list', 'fra')

    def test_error_no_match(self):
        self.assert_status(SUCCESS, 'language', 'new', 'fra', 'French')
        self.assert_status(NOT_FOUND, 'lexpat', 'list', 'fra')

    def test_error_invalid_code(self):
        self.assert_status(SUCCESS, 'language', 'new', 'fra', 'French')
        self.assert_status(INVALID, 'lexpat', 'new', 'fr', 'X *donner* Y à Z_hum', '--force-lemma')

    def test_error_language_not_found(self):
        self.assert_status(NOT_FOUND, 'lexpat', 'new', 'fra', 'X *donner* Y à Z_hum', '--force-lemma')


class DeleteCommand(TestCase):
    def test_success(self):
        lang = Language(code='fra', name='French'); lang.save()
        unit = LexicalUnit(user_id=1, language=lang, lemma='donner'); unit.save()
        pat  = LexicalPattern(lexical_unit=unit, description='X *donner* Y à Z_hum'); pat.save()
        self.assert_status(SUCCESS, 'lexpat', 'delete', pat.id)

    def test_error_lexical_unit_not_found(self):
        self.assert_status(NOT_FOUND, 'lexpat', 'delete', 123)


class ModifyCommand(TestCase):
    def test_success(self):
        lang = Language(code='fra', name='French'); lang.save()
        unit = LexicalUnit(user_id=1, language=lang, lemma='donner'); unit.save()
        pat  = LexicalPattern(lexical_unit=unit, description='X *donner* Y'); pat.save()
        self.assert_status(SUCCESS, 'lexpat', 'modify', pat.id, '-d', 'X *donner* Y à Z_hum')

    def test_error_lexical_unit_not_found(self):
        self.assert_status(NOT_FOUND, 'lexpat', 'delete', 123)


class InfoCommand(TestCase):
    def test_success(self):
        User(id=1, username='maxime').save()
        lang = Language(code='fra', name='French'); lang.save()
        unit = LexicalUnit(user_id=1, language=lang, lemma='donner'); unit.save()
        pat  = LexicalPattern(lexical_unit=unit, description='X *donner* Y'); pat.save()
        self.assert_status(SUCCESS, 'lexpat', 'info', pat.id)

    def test_error_not_found(self):
        self.assert_status(NOT_FOUND, 'lexpat', 'info', 123)
