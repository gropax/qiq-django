from django.contrib.auth.models import User
from qiq.test import TestCase
from qiq.common import SUCCESS, INVALID, EXISTS, NOT_FOUND
from notes.models import Note, Document


class NewCommand(TestCase):
    def test_success(self):
        note = Note(user_id=1, text='abc', original=True)
        note.save()
        self.assert_success('document', 'new', 'mydoc', note.id)

    def test_invalid_name(self):
        self.assert_invalid('document', 'new', '3mydoc', 123)
        self.assert_invalid('document', 'new', '.mydoc', 123)
        self.assert_invalid('document', 'new', 'mydoc.', 123)

    def test_already_exists(self):
        note = Note(user_id=1, text='abc', original=True)
        note.save()
        self.assert_success('document', 'new', 'mydoc', note.id)
        self.assert_exists('document', 'new', 'mydoc', note.id)

    def test_note_not_found(self):
        self.assert_not_found('document', 'new', 'mydoc', 123)

    def test_note_not_original(self):
        note = Note(user_id=1, text='abc', original=False)
        note.save()
        self.assert_invalid('document', 'new', 'mydoc', note.id)


class InfoCommand(TestCase):
    def test_success(self):
        User(username='auie').save()
        note = Note(user_id=1, text='abc', original=True); note.save()
        doc = Document(user_id=1, note=note, name='abc'); doc.save()
        self.assert_success('document', 'info', note.id)

    def test_error_not_found(self):
        self.assert_not_found('document', 'info', 123)


class ListCommand(TestCase):
    def test_success(self):
        note = Note(user_id=1, text='abc', original=True); note.save()
        doc = Document(user_id=1, note=note, name='abc'); doc.save()
        self.assert_success('document', 'list')

    def test_error_no_match(self):
        self.assert_not_found('document', 'list')


class ModifyCommand(TestCase):
    def test_success(self):
        note = Note(user_id=1, text='abc', original=True); note.save()
        doc = Document(user_id=1, note=note, name='abc'); doc.save()
        self.assert_success('document', 'modify', 'abc', '-d', '"desc"')
        self.assert_success('document', 'modify', 'abc', '-n', 'def')
        self.assert_success('document', 'modify', 'def', '-n', 'abc', '-d', "'desc'")
        self.assert_success('document', 'modify', doc.id, '-d', '"desc2"')
        self.assert_success('document', 'modify', doc.id, '-d', '"desc2"')

    def test_error_document_not_found(self):
        self.assert_not_found('document', 'modify', 'abc', '-n', 'def')
        self.assert_not_found('document', 'modify', '123', '-n', 'def')

    def test_error_invalid_name(self):
        note = Note(user_id=1, text='abc', original=True); note.save()
        doc = Document(user_id=1, note=note, name='abc'); doc.save()
        self.assert_invalid('document', 'modify', 'abc', '-n', '.auie')


class DeleteCommand(TestCase):
    def test_success(self):
        note = Note(user_id=1, text='abc', original=True); note.save()
        doc = Document(user_id=1, note=note, name='abc'); doc.save()
        self.assert_success('document', 'delete', 'abc')

        doc = Document(user_id=1, note=note, name='abc'); doc.save()
        self.assert_success('document', 'delete', doc.id)

    def test_error_document_not_found(self):
        self.assert_not_found('document', 'delete', 'abc')
        self.assert_not_found('document', 'delete', 123)
