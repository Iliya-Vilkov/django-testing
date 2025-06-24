from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()

NOTE_SLUG = 'slug'
NOTE_TEXT = 'Текст заметки'
NOTE_TITLE = 'Текст заголовка'
ADD_URL = reverse('notes:add')
EDIT_URL = reverse('notes:edit', args=[NOTE_SLUG])
DETAIL_URL = reverse('notes:detail', args=[NOTE_SLUG])
DELETE_URL = reverse('notes:delete', args=[NOTE_SLUG])
HOME_URL = reverse('notes:home')
LIST_URL = reverse('notes:list')
SUCCESS_URL = reverse('notes:success')
LOGIN_URL = reverse('users:login')
LOGOUT_URL = reverse('users:logout')
SIGNUP_URL = reverse('users:signup')
REDIRECT_LIST_URL = f'{LOGIN_URL}?next={LIST_URL}'
REDIRECT_ADD_URL = f'{LOGIN_URL}?next={ADD_URL}'
REDIRECT_DETAIL_URL = f'{LOGIN_URL}?next={DETAIL_URL}'
REDIRECT_DELETE_URL = f'{LOGIN_URL}?next={DELETE_URL}'
REDIRECT_EDIT_URL = f'{LOGIN_URL}?next={EDIT_URL}'


class BaseTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Илья Вилков')
        cls.reader = User.objects.create(username='Илья')
        cls.note = Note.objects.create(title=NOTE_TITLE,
                                       text=NOTE_TEXT,
                                       slug=NOTE_SLUG,
                                       author=cls.author)
        cls.form_data = {
            'title': NOTE_TITLE,
            'text': NOTE_TEXT,
            'slug': NOTE_SLUG
        }
        cls.author_client = Client()
        cls.reader_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader_client.force_login(cls.reader)
