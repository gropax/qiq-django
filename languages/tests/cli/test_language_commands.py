from qiq.test import TestCase
from languages.models import Language


class NewCommand(TestCase):
    def test_created(self):
        self.assert_success('language', 'new', 'fra', 'French')

    def test_error_invalid_code(self):
        self.assert_invalid('language', 'new', 'fr', 'French')
        self.assert_invalid('language', 'new', 'fr3', 'French')

    def test_error_already_exists(self):
        self.assert_success('language', 'new', 'fra', 'French')
        self.assert_exists('language', 'new', 'fra', 'French')


class ListCommand(TestCase):
    def test_success(self):
        self.assert_success('language', 'new', 'fra', 'French')
        self.assert_success('language', 'list')

    def test_error_no_match(self):
        self.assert_not_found('language', 'list')


class ModifyCommand(TestCase):
    def test(self):
        self.assert_not_implemented('language', 'modify')

class DeletelCommand(TestCase):
    def test(self):
        self.assert_not_implemented('language', 'delete')

class InfoCommand(TestCase):
    def test(self):
        self.assert_not_implemented('language', 'info')
