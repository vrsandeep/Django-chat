from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test.utils import override_settings

from .models import Chat
from .views import chat_room


class TestView(TestCase):

    @override_settings(DEBUG=True)
    def test_chat_room(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', password='top_secret')

        request = self.factory.get(reverse('chat_room', kwargs={"room": "public"}))
        request.user = self.user

        r = chat_room(request, 'public')
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Django Chat Channels')
