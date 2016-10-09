from django.contrib.auth.models import User
from qiq.test import TestCase
from notes.models import Note
from projects.models import Project


class NewCommand(TestCase):
    def test_success(self):
        path = self.dummy_file()
        self.assert_success('note', 'new', '-P', '-f', path)
        self.assert_success('note', 'new', '-c', '-p', 'proj', '-f', path)


class InfoCommand(TestCase):
    def test_success(self):
        User(username='auie').save()
        note = Note(user_id=1, text='abc', original=True); note.save()
        self.assert_success('note', 'info', note.id)

    def test_error_not_found(self):
        self.assert_not_found('note', 'info', 123)


class ListCommand(TestCase):
    def test_success(self):
        User(username='auie').save()
        note = Note(user_id=1, text='abc', original=True); note.save()
        self.assert_success('note', 'list')

        prj = Project(user_id=1, name='myproject'); prj.save()
        note = Note(user_id=1, project=prj, text='abc', original=True); note.save()
        self.assert_success('note', 'list', 'proj:myproject')

    def test_error_no_match(self):
        self.assert_not_found('note', 'list')


class DeleteCommand(TestCase):
    def test_success(self):
        User(username='auie').save()
        note = Note(user_id=1, text='abc', original=True); note.save()
        self.assert_success('note', 'delete', note.id)

    def test_error_no_match(self):
        self.assert_not_found('note', 'delete', 123)


class MergeCommand(TestCase):
    def test_success_selected_by_id(self):
        User(username='auie').save()
        note1 = Note(user_id=1, text='abc', original=True); note1.save()
        note2 = Note(user_id=1, text='def', original=True); note2.save()

        path = self.dummy_file()
        ids = "%i,%i" % (note1.id, note2.id)
        self.assert_success('note', 'merge', ids, '-P', '-q')

    def test_error_no_match(self):
        self.assert_not_found('note', 'delete', 123)


#class SplitCommand(TestCase):
    #def test_success_selected_by_id(self):
        #User(username='auie').save()
        #note = Note(user_id=1, text='abcdef', original=True); note.save()

        #path = dummy_note_file()
        #ids = "%i,%i" % (note1.id, note2.id)
        #self.assert_success('note', 'merge', ids, '-P', '-q')

    #def test_error_no_match(self):
        #self.assert_not_found('note', 'delete', 123)


class GetCommand(TestCase):
    def test_success(self):
        User(username='auie').save()
        note = Note(user_id=1, text='abc', original=True); note.save()
        self.assert_success('note', 'get', 'text', note.id)

    def test_error_no_match(self):
        self.assert_not_found('note', 'get', 'text', 123)


class StatusCommand(TestCase):
    def test_success(self):
        self.assert_success('note', 'status')
