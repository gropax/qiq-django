from qiq.test import TestCase
from qiq.common import SUCCESS, INVALID, EXISTS, NOT_FOUND
from languages.models import Language


class NewCommand(TestCase):
    def test_created(self):
        self.assert_status(SUCCESS, 'language', 'new', 'fra', 'French')

    def test_error_invalid_code(self):
        self.assert_status(INVALID, 'language', 'new', 'fr', 'French')
        self.assert_status(INVALID, 'language', 'new', 'fr3', 'French')

    def test_error_already_exists(self):
        self.assert_status(SUCCESS, 'language', 'new', 'fra', 'French')
        self.assert_status(EXISTS, 'language', 'new', 'fra', 'French')


class ListCommand(TestCase):
    def test_success(self):
        self.assert_status(SUCCESS, 'language', 'new', 'fra', 'French')
        self.assert_status(SUCCESS, 'language', 'list')

    def test_error_no_match(self):
        self.assert_status(NOT_FOUND, 'language', 'list')

#class ModifyCommand(TestCase):
    #def test_success(self):
        #self.assert_status(SUCCESS, 'project', 'new', 'proj')
        #self.assert_status(SUCCESS, 'project', 'modify', 'proj', '-d', '"desc"')
        #self.assert_status(SUCCESS, 'project', 'modify', 'proj', '-n', 'proj2')
        #self.assert_status(SUCCESS, 'project', 'modify', 'proj2', '-n', 'proj3', '-d', '"desc2"')
        #self.assert_status(SUCCESS, 'project', 'modify', 'proj3', '-n', 'proj3')

        #proj = Project(user_id=1, name='abc'); proj.save()
        #self.assert_status(SUCCESS, 'project', 'modify', proj.id, '-n', 'def')

    #def test_error_invalid_name(self):
        #self.assert_status(INVALID, 'project', 'modify', 'proj.sub', '-n', 'name')
        #self.assert_status(INVALID, 'project', 'modify', '/proj', '-n', 'name')
        #self.assert_status(SUCCESS, 'project', 'new', 'proj')
        #self.assert_status(INVALID, 'project', 'modify', 'proj', '-n', '/name')

    #def test_error_project_not_found(self):
        #self.assert_status(NOT_FOUND, 'project', 'modify', 'proj', '-d', '"auie"')


#class InfoCommand(TestCase):
    #def test_success(self):
        #proj = Project(user_id=1, name='abc'); proj.save()
        #self.assert_status(SUCCESS, 'project', 'info', proj.id)
        #self.assert_status(SUCCESS, 'project', 'info', proj.name)

    #def test_error_not_found(self):
        #self.assert_status(NOT_FOUND, 'project', 'info', 123)
        #self.assert_status(NOT_FOUND, 'project', 'info', 'myproj')
