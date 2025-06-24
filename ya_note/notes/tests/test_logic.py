from http import HTTPStatus

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from notes.tests.base_test_case import (
    BaseTest,
    ADD_URL,
    EDIT_URL,
    SUCCESS_URL,
    DELETE_URL
)


class TestNoteLogic(BaseTest):
    NOTE_TITLE = 'title'
    NOTE_SLUG = 'slug'
    NOTE_TEXT = 'text'

    def test_user_can_create_note(self):
        notes = set(Note.objects.all())
        self.author_client.post(
            ADD_URL, data=self.form_data
        )
        self.assertEqual(len(notes), 1)
        note = notes.pop()
        self.assertEqual(note.slug, self.form_data[self.NOTE_SLUG])
        self.assertEqual(note.title, self.form_data[self.NOTE_TITLE])
        self.assertEqual(note.text, self.form_data[self.NOTE_TEXT])
        self.assertEqual(note.author, self.author)

    def test_anonymous_user_cannot_create_note(self):
        notes = set(Note.objects.all())
        self.assertEqual(self.client.post(
            ADD_URL, data=self.form_data
        ).status_code, HTTPStatus.FOUND)
        self.assertEqual(set(Note.objects.all()), notes)

    def test_not_unique_slug(self):
        self.notes_counts = Note.objects.count()
        self.form_data['slug'] = self.note.slug
        response = self.author_client.post(ADD_URL,
                                           data=self.form_data)
        self.assertFormError(response.context['form'], 'slug',
                             errors=self.note.slug + WARNING)
        self.assertEqual(Note.objects.count(), self.notes_counts)

    def test_empty_slug(self):
        self.form_data.pop(self.NOTE_SLUG)
        notes = set(Note.objects.all())
        self.author_client.post(
            ADD_URL, data=self.form_data
        )
        notes = set(Note.objects.all()) - notes
        self.assertEqual(len(notes), 1)
        note = notes.pop()
        self.assertEqual(note.title, self.form_data[self.NOTE_TITLE])
        self.assertEqual(note.text, self.form_data[self.NOTE_TEXT])
        self.assertEqual(
            note.slug, slugify(self.form_data[self.NOTE_TITLE])
        )
        self.assertEqual(note.author, self.author)

    def test_author_can_edit_note(self):
        response = self.author_client.post(EDIT_URL, data=self.form_data)
        self.assertRedirects(response, SUCCESS_URL)
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.slug, self.form_data[self.NOTE_SLUG])
        self.assertEqual(note.title, self.form_data[self.NOTE_TITLE])
        self.assertEqual(note.text, self.form_data[self.NOTE_TEXT])
        self.assertEqual(note.author, self.note.author)

    def test_author_can_delete_note(self):
        notes = set(Note.objects.all())
        self.author_client.post(
            DELETE_URL, data=self.form_data
        )
        self.assertEqual(len(notes - set(Note.objects.all())), 1)

    def test_user_cant_edit_note_of_another_user(self):
        note = Note.objects.get(id=self.note.id)
        response = self.reader_client.post(EDIT_URL, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.author, self.note.author)

    def test_user_cant_delete_note_of_another_user(self):
        response = self.reader_client.delete(DELETE_URL, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.author, self.note.author)
