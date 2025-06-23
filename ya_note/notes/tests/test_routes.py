from http import HTTPStatus

from notes.tests.base_test_case import (BaseTest,
                                        ADD_URL,
                                        EDIT_URL,
                                        DETAIL_URL,
                                        DELETE_URL,
                                        HOME_URL,
                                        LIST_URL,
                                        SUCCESS_URL,
                                        LOGIN_URL,
                                        LOGOUT_URL,
                                        SIGNUP_URL,
                                        REDIRECT_LIST_URL,
                                        REDIRECT_ADD_URL,
                                        REDIRECT_DETAIL_URL,
                                        REDIRECT_DELETE_URL,
                                        REDIRECT_EDIT_URL)


class TestRoutes(BaseTest):
    def test_pages_availability(self):
        users_statuses = [
            (ADD_URL, self.client, HTTPStatus.FOUND),
            (EDIT_URL, self.client, HTTPStatus.FOUND),
            (DETAIL_URL, self.client, HTTPStatus.FOUND),
            (DELETE_URL, self.client, HTTPStatus.FOUND),
            (HOME_URL, self.client, HTTPStatus.OK),
            (LIST_URL, self.client, HTTPStatus.FOUND),
            (LOGIN_URL, self.client, HTTPStatus.OK),
            (LOGOUT_URL, self.client, HTTPStatus.OK),
            (SIGNUP_URL, self.client, HTTPStatus.OK),

            (EDIT_URL, self.author_client, HTTPStatus.OK),
            (DETAIL_URL, self.author_client, HTTPStatus.OK),
            (DELETE_URL, self.author_client, HTTPStatus.OK),
            (LOGIN_URL, self.author_client, HTTPStatus.OK),
            (LOGOUT_URL, self.author_client, HTTPStatus.OK),
            (SIGNUP_URL, self.author_client, HTTPStatus.OK),

            (ADD_URL, self.reader_client, HTTPStatus.OK),
            (EDIT_URL, self.reader_client, HTTPStatus.NOT_FOUND),
            (DETAIL_URL, self.reader_client, HTTPStatus.NOT_FOUND),
            (DELETE_URL, self.reader_client, HTTPStatus.NOT_FOUND),
            (LIST_URL, self.reader_client, HTTPStatus.OK),
            (SUCCESS_URL, self.reader_client, HTTPStatus.OK),
            (LOGIN_URL, self.reader_client, HTTPStatus.OK),
            (LOGOUT_URL, self.reader_client, HTTPStatus.OK),
            (SIGNUP_URL, self.reader_client, HTTPStatus.OK),
        ]

        for url, client, expected_status in users_statuses:
            if url == LOGOUT_URL:
                assert client.post(url).status_code == HTTPStatus.OK
            else:
                with self.subTest(url=url, client=client):
                    self.assertEqual(
                        client.get(url).status_code,
                        expected_status,
                    )

    def test_redirect_for_anonymous_client(self):
        redirect_list = [
            (LIST_URL, REDIRECT_LIST_URL),
            (ADD_URL, REDIRECT_ADD_URL),
            (DETAIL_URL, REDIRECT_DETAIL_URL),
            (DELETE_URL, REDIRECT_DELETE_URL),
            (EDIT_URL, REDIRECT_EDIT_URL)
        ]

        for url, redirect_url in redirect_list:
            with self.subTest(name=url):
                self.assertRedirects(
                    self.client.get(url),
                    redirect_url
                )
