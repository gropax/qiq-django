from qiq.test import TestCase
from projects.models import Project


class NewCommand(TestCase):
    def test_created(self):
        self.assert_success('project', 'new', 'proj')
        self.assert_success('project', 'new', 'proj_auie')

    def test_created_with_description(self):
        self.assert_success('project', 'new', 'proj', '-d', '"my desc"')

    def test_created_recursively(self):
        self.assert_success('project', 'new', 'glparent/parent/child')

    def test_error_already_exists(self):
        self.assert_success('project', 'new', 'proj')
        self.assert_exists('project', 'new', 'proj')

    def test_error_invalid_name(self):
        self.assert_invalid('project', 'new', 'proj.sub')
        self.assert_invalid('project', 'new', '1proj')
        self.assert_invalid('project', 'new', '/proj')
        self.assert_invalid('project', 'new', 'proj/')


class ListCommand(TestCase):
    def test_success(self):
        self.assert_success('project', 'new', 'proj')
        self.assert_success('project', 'list')

    def test_error_no_match(self):
        self.assert_not_found('project', 'list')


class ModifyCommand(TestCase):
    def test_success(self):
        self.assert_success('project', 'new', 'proj')
        self.assert_success('project', 'modify', 'proj', '-d', '"desc"')
        self.assert_success('project', 'modify', 'proj', '-n', 'proj2')
        self.assert_success('project', 'modify', 'proj2', '-n', 'proj3', '-d', '"desc2"')
        self.assert_success('project', 'modify', 'proj3', '-n', 'proj3')

        proj = Project(user_id=1, name='abc'); proj.save()
        self.assert_success('project', 'modify', proj.id, '-n', 'def')

    def test_error_invalid_name(self):
        self.assert_invalid('project', 'modify', 'proj.sub', '-n', 'name')
        self.assert_invalid('project', 'modify', '/proj', '-n', 'name')
        self.assert_success('project', 'new', 'proj')
        self.assert_invalid('project', 'modify', 'proj', '-n', '/name')

    def test_error_project_not_found(self):
        self.assert_not_found('project', 'modify', 'proj', '-d', '"auie"')


class DeleteCommand(TestCase):
    def test_success(self):
        self.assert_success('project', 'new', 'proj')
        self.assert_success('project', 'delete', 'proj')

        proj = Project(user_id=1, name='abc'); proj.save()
        self.assert_success('project', 'delete', proj.id)

    def test_error_invalid_name(self):
        self.assert_invalid('project', 'delete', 'proj.sub')
        self.assert_invalid('project', 'delete', '/proj')

    def test_error_project_not_found(self):
        self.assert_not_found('project', 'delete', 'proj')


class InfoCommand(TestCase):
    def test_success(self):
        proj = Project(user_id=1, name='abc'); proj.save()
        self.assert_success('project', 'info', proj.id)
        self.assert_success('project', 'info', proj.name)

    def test_error_not_found(self):
        self.assert_not_found('project', 'info', 123)
        self.assert_not_found('project', 'info', 'myproj')
