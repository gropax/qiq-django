from qiq.test import TestCase
from qiq.common import SUCCESS, INVALID, EXISTS, NOT_FOUND
from projects.models import Project


class NewCommand(TestCase):
    def test_created(self):
        self.assert_status(SUCCESS, 'project', 'new', 'proj')
        self.assert_status(SUCCESS, 'project', 'new', 'proj_auie')

    def test_created_with_description(self):
        self.assert_status(SUCCESS, 'project', 'new', 'proj', '-d', '"my desc"')

    def test_created_recursively(self):
        self.assert_status(SUCCESS, 'project', 'new', 'glparent/parent/child')

    def test_error_already_exists(self):
        self.assert_status(SUCCESS, 'project', 'new', 'proj')
        self.assert_status(EXISTS, 'project', 'new', 'proj')

    def test_error_invalid_name(self):
        self.assert_status(INVALID, 'project', 'new', '1proj')
        self.assert_status(INVALID, 'project', 'new', '/proj')
        self.assert_status(INVALID, 'project', 'new', 'proj/')

class ListCommand(TestCase):
    def test_success(self):
        self.assert_status(SUCCESS, 'project', 'new', 'proj')
        self.assert_status(SUCCESS, 'project', 'list')

    def test_error_no_match(self):
        self.assert_status(NOT_FOUND, 'project', 'list')

class ModifyCommand(TestCase):
    def test_success(self):
        self.assert_status(SUCCESS, 'project', 'new', 'proj')
        self.assert_status(SUCCESS, 'project', 'modify', 'proj', '-d', '"desc"')
        self.assert_status(SUCCESS, 'project', 'modify', 'proj', '-n', 'proj2')
        self.assert_status(SUCCESS, 'project', 'modify', 'proj2', '-n', 'proj3', '-d', '"desc2"')
        self.assert_status(SUCCESS, 'project', 'modify', 'proj3', '-n', 'proj3')

    def test_error_invalid_name(self):
        self.assert_status(INVALID, 'project', 'modify', '/proj', '-n', 'name')
        self.assert_status(SUCCESS, 'project', 'new', 'proj')
        self.assert_status(INVALID, 'project', 'modify', 'proj', '-n', '/name')

    def test_error_project_not_found(self):
        self.assert_status(NOT_FOUND, 'project', 'modify', 'proj', '-d', '"auie"')