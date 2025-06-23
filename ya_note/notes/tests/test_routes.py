from http import HTTPStatus
from django.urls import reverse

from notes.tests.base_test_case import BaseTest


class TestRoutes(BaseTest):

    def test_pages_availability(self):
        urls = (
            ('notes:home'),
            ('users:login'),
            ('users:signup'),
        )
        for name in urls:
            with self.subTest(name=name):
                url = reverse(name)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_note_show_and_edit_and_delete(self):
        users_statuses = (
            (self.author_client, HTTPStatus.OK),
            (self.reader_client, HTTPStatus.NOT_FOUND),
        )
        for user, status in users_statuses:
            for name in ('notes:detail', 'notes:edit', 'notes:delete'):
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=(self.note.slug,))
                    response = user.get(url)
                    self.assertEqual(response.status_code, status)

    def test_availability_for_note_add_and_list(self):
        urls = (
            ('notes:add'),
            ('notes:list'),
            ('notes:success'),
        )
        for name in urls:
            with self.subTest(name=name):
                url = reverse(name)
                response = self.author_client.get(url)
            self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_redirect_for_anonymous_client(self):
        login_url = reverse('users:login')
        urls = (
            ('notes:detail', (self.note.slug,)),
            ('notes:edit', (self.note.slug,)),
            ('notes:delete', (self.note.slug,)),
            ('notes:add', None),
            ('notes:list', None),
            ('notes:success', None),
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
