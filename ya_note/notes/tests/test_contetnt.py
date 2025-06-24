from notes.forms import NoteForm
from notes.tests.base_test_case import (BaseTest,
                                        LIST_URL,
                                        ADD_URL,
                                        EDIT_URL)


class TestContent(BaseTest):

    def test_notes_list_for_auth_user(self):
        response = self.author_client.get(LIST_URL)
        notes = response.context['object_list']
        self.assertIn(self.note, notes)

    def test_notes_list_for_anonymous_user(self):
        response = self.reader_client.get(LIST_URL)
        notes = response.context['object_list']
        self.assertNotIn(self.note, notes)

    def test_create_and_add_note_pages_contains_form(self):
        urls = (
            (ADD_URL),
            (EDIT_URL)
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
