from http import HTTPStatus

import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

FORM_COMMENT = {'text': 'Текст'}
FORM_DATA = {'text': 'Текст'}

pytestmark = pytest.mark.django_db


def test_anonymous_user_cant_create_comment(client, news_detail_url,
                                            user_login_url):
    response = client.post(news_detail_url, data=FORM_DATA)
    expected_url = f'{user_login_url}?next={news_detail_url}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 0


def test_user_can_create_comment(
        author_client, author, news_detail_url):
    response = author_client.post(news_detail_url, data=FORM_DATA)
    expected_url = f'{news_detail_url}#comments'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
    assert new_comment.text == FORM_DATA['text']
    assert new_comment.author == author


def test_user_cant_use_bad_words(admin_client, news_detail_url):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = admin_client.post(news_detail_url, data=bad_words_data)
    assertFormError(
        response.context['form'],
        field='text',
        errors=WARNING
    )
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_delete_comment(
        author_client, news_detail_url, comment_delete_url):
    url_to_comments = f'{news_detail_url}#comments'
    response = author_client.delete(comment_delete_url)
    assertRedirects(response, url_to_comments)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_edit_comment(author_client, comment, comment_edit_url,
                                 news, author):
    author_client.post(comment_edit_url, data=FORM_COMMENT)
    updated_comment = Comment.objects.get(pk=comment.pk)
    assert updated_comment.text == FORM_COMMENT['text']
    assert updated_comment.news == news
    assert updated_comment.author == author


def test_user_cant_edit_comment_of_another_user(
    not_author_client, comment, comment_edit_url
):
    assert (
        not_author_client.post(comment_edit_url, data=FORM_COMMENT)
        .status_code == HTTPStatus.NOT_FOUND
    )
    expected_comment = Comment.objects.get(pk=comment.pk)
    assert expected_comment.text == comment.text
    assert expected_comment.author == comment.author
    assert expected_comment.news == comment.news


def test_user_cant_delete_comment_of_another_user(
    not_author_client, comment, comment_delete_url
):
    assert (
        not_author_client.delete(comment_delete_url)
        .status_code == HTTPStatus.NOT_FOUND
    )
    assert Comment.objects.filter(pk=comment.pk).exists()
    expected_comment = Comment.objects.get(pk=comment.pk)
    assert expected_comment.text == comment.text
    assert expected_comment.author == comment.author
    assert expected_comment.news == comment.news
    assert Comment.objects.count() == 1
