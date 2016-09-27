from qiq.test import TestCase
from qiq.common import SUCCESS, INVALID, EXISTS, NOT_FOUND
from notes.models import Note
from projects.models import Project
from django.contrib.auth.models import User


class NewCommand(TestCase):
    def test_success(self):
        pass
        #self.assert_status(SUCCESS, 'note', 'new', '-P')
        #self.assert_status(SUCCESS, 'note', 'new', '-p', 'proj', '-c')
        #self.assert_status(SUCCESS, 'note', 'new', '-P', '-f', 'file.txt')


class InfoCommand(TestCase):
    def test_success(self):
        User(username='auie').save()
        note = Note(user_id=1, text='abc', original=True); note.save()
        self.assert_status(SUCCESS, 'note', 'info', note.id)

    def test_error_not_found(self):
        self.assert_status(NOT_FOUND, 'note', 'info', 123)


class ListCommand(TestCase):
    def test_success(self):
        User(username='auie').save()
        note = Note(user_id=1, text='abc', original=True); note.save()
        self.assert_status(SUCCESS, 'note', 'list')

        prj = Project(user_id=1, name='myproject'); prj.save()
        note = Note(user_id=1, project=prj, text='abc', original=True); note.save()
        self.assert_status(SUCCESS, 'note', 'list', 'proj:myproject')

    def test_error_no_match(self):
        self.assert_status(NOT_FOUND, 'note', 'list')


class DeleteCommand(TestCase):
    def test_success(self):
        User(username='auie').save()
        note = Note(user_id=1, text='abc', original=True); note.save()
        self.assert_status(SUCCESS, 'note', 'delete', note.id)

    def test_error_no_match(self):
        self.assert_status(NOT_FOUND, 'note', 'delete', 123)


class MergeCommand(TestCase):
    #def test_success(self):
        #User(username='auie').save()
        #note = Note(user_id=1, text='abc', original=True); note.save()
        #self.assert_status(SUCCESS, 'note', 'delete', note.id)

    def test_error_no_match(self):
        self.assert_status(NOT_FOUND, 'note', 'delete', 123)


class GetCommand(TestCase):
    def test_success(self):
        User(username='auie').save()
        note = Note(user_id=1, text='abc', original=True); note.save()
        self.assert_status(SUCCESS, 'note', 'get', 'text', note.id)

    def test_error_no_match(self):
        self.assert_status(NOT_FOUND, 'note', 'get', 'text', 123)
