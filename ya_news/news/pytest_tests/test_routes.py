from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects
from pytest_lazy_fixtures import lf


CLIENT = lf('client')
NOT_AUTHOR_CLIENT = lf('not_author_client')
AUTHOR_CLIENT = lf('author_client')
NEWS_HOME = lf('news_home_url')
NEWS_DETAIL = lf('news_detail_url')
USER_LOGIN = lf('user_login_url')
USER_LOGOUT = lf('user_logout_url')
USER_SIGNUP = lf('user_signup_url')
COMMENT_EDIT = lf('comment_edit_url')
COMMENT_DELETE = lf('comment_delete_url')
REDIRECT_EDIT_URL = lf('redirect_edit_url')
REDIRECT_DELETE_URL = lf('redirect_delete_url')


@pytest.mark.parametrize(
    'url, method, client_fixture, expected_status',
    [
        (NEWS_HOME, 'get', CLIENT, HTTPStatus.OK),
        (NEWS_DETAIL, 'get', CLIENT, HTTPStatus.OK),
        (USER_LOGIN, 'get', CLIENT, HTTPStatus.OK),
        (USER_LOGOUT, 'post', CLIENT, HTTPStatus.OK),
        (USER_SIGNUP, 'get', CLIENT, HTTPStatus.OK),
        (COMMENT_EDIT, 'get', CLIENT, HTTPStatus.FOUND),
        (COMMENT_DELETE, 'get', CLIENT, HTTPStatus.FOUND),
        (COMMENT_EDIT, 'get', NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND),
        (COMMENT_DELETE, 'get', NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND),
        (COMMENT_EDIT, 'get', AUTHOR_CLIENT, HTTPStatus.OK),
        (COMMENT_DELETE, 'get', AUTHOR_CLIENT, HTTPStatus.OK),
    ],
)
def test_pages_availability(url, method, client_fixture, expected_status):
    assert getattr(client_fixture, method)(url).status_code == expected_status


@pytest.mark.parametrize(
    'url, redirect_url',
    [
        (COMMENT_EDIT, REDIRECT_EDIT_URL),
        (COMMENT_DELETE, REDIRECT_DELETE_URL),
    ]
)
def test_redirect_for_anonymous_users(client, url, redirect_url):
    assertRedirects(client.get(url), redirect_url)
