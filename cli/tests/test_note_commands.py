from qiq.test import TestCase
from qiq.common import SUCCESS, INVALID, EXISTS, NOT_FOUND
from notes.models import Note
from projects.models import Project
from django.contrib.auth.models import User
import tempfile


def dummy_note_file(text='abc'):
    _, path = tempfile.mkstemp()
    with open(path, 'w') as f:
        f.write(text)
    return path


class NewCommand(TestCase):
    def test_success(self):
        path = dummy_note_file()
        self.assert_status(SUCCESS, 'note', 'new', '-P', '-f', path)
        self.assert_status(SUCCESS, 'note', 'new', '-c', '-p', 'proj', '-f', path)


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
    def test_success_selected_by_id(self):
        User(username='auie').save()
        note1 = Note(user_id=1, text='abc', original=True); note1.save()
        note2 = Note(user_id=1, text='def', original=True); note2.save()

        path = dummy_note_file()
        ids = "%i,%i" % (note1.id, note2.id)
        self.assert_status(SUCCESS, 'note', 'merge', ids, '-P', '-q')

    def test_error_no_match(self):
        self.assert_status(NOT_FOUND, 'note', 'delete', 123)


#class SplitCommand(TestCase):
    #def test_success_selected_by_id(self):
        #User(username='auie').save()
        #note = Note(user_id=1, text='abcdef', original=True); note.save()

        #path = dummy_note_file()
        #ids = "%i,%i" % (note1.id, note2.id)
        #self.assert_status(SUCCESS, 'note', 'merge', ids, '-P', '-q')

    #def test_error_no_match(self):
        #self.assert_status(NOT_FOUND, 'note', 'delete', 123)


class GetCommand(TestCase):
    def test_success(self):
        User(username='auie').save()
        note = Note(user_id=1, text='abc', original=True); note.save()
        self.assert_status(SUCCESS, 'note', 'get', 'text', note.id)

    def test_error_no_match(self):
        self.assert_status(NOT_FOUND, 'note', 'get', 'text', 123)
