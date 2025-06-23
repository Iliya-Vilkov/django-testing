from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()

NOTE_SLUG = 'slug'
NOTE_TEXT = 'Текст заметки'
NOTE_TITLE = 'Текст заголовка'
NEW_NOTE_TEXT = 'Обновлённая заметка'
NEW_NOTE_TITLE = 'Обновлённый заголовок заметки'
NEW_NOTE_SLUG = 'new_slug'
ADD_URL = reverse('notes:add')
EDIT_URL = reverse('notes:edit', args=[NOTE_SLUG])
DETAIL_URL = reverse('notes:detail', args=[NOTE_SLUG])
DELETE_URL = reverse('notes:delete', args=[NOTE_SLUG])
HOME_URL = reverse('notes:home')
LIST_URL = reverse('notes:list')
SUCCES_URL = reverse('notes:success')
LOGIN_URL = reverse('users:login')
LOGAUT_URL = reverse('users:logaut')
SIGUP_URL = reverse('users:signuip')
REDIRECT_LIST_URL = f'{LOGIN_URL}?next={LIST_URL}'
REDIRECT_ADD_URL = f'{LOGIN_URL}?next={ADD_URL}'
REDIRECT_DETAIL_URL = f'{LOGIN_URL}?next={DETAIL_URL}'
REDIRECT_DELETE_URL = f'{LOGIN_URL}?next={DELETE_URL}'
REDIRECT_EDIT_URL = f'{LOGIN_URL}?next={EDIT_URL}'


class BaseTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Илья Вилков')
        cls.note = Note.objects.create(title='Заголовок',
                                       text='Текст',
                                       author=cls.author)
        cls.reader = User.objects.create(username='Илья')
        cls.form_data = {'text': cls.NOTE_TEXT, 'title': cls.NOTE_TITLE,
                         'slug': cls.NOTE_SLUG, 'author': cls.auth_client}
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
