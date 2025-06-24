import pytest

from news.forms import CommentForm
from yanews.settings import NEWS_COUNT_ON_HOME_PAGE

pytestmark = pytest.mark.django_db


def test_news_count(client, news_list, news_home_url):
    response = client.get(news_home_url)
    object_list = response.context['object_list']
    assert "news_list" in response.context
    news_count = object_list.count()
    assert news_count is NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, news_home_url):
    response = client.get(news_home_url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(author_client, comments, news_detail_url):
    comments = (author_client.get(news_detail_url).
                context['news'].comment_set.all())
    all_comments = [comment.created for comment in comments]
    sorted_comments = sorted(all_comments)
    assert all_comments == sorted_comments


def test_form_availability_for_different_users(author_client, news_detail_url):
    response = author_client.get(news_detail_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
