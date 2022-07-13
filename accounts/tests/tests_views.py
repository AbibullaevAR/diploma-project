from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from accounts.views import MentorRegistrationView, ChangeProfileView
from accounts.tests.tests_models import UserModelTest


class MentorRegistrationViewTest(TestCase):

    def test_get_request(self):
        resp = self.client.get(reverse('accounts:mentor_registration'))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.resolver_match.func.__name__, MentorRegistrationView.as_view().__name__)

        self.assertTemplateUsed(resp, 'accounts/MentorRegistrationTemplate.html')

    def test_post_create_mentor(self):
        resp = self.client.post(
            reverse('accounts:mentor_registration'),
            data={'email': 'test@mail.ru', 'group': 'test_group'},
            follow=True
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.resolver_match.func.__name__, MentorRegistrationView.as_view().__name__)

        self.assertRedirects(resp, reverse('accounts:login'))
        self.assertEqual(len(mail.outbox), 1)


class ChangeProfileViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        UserModelTest.setUpTestData()

    def test_get_request(self):
        self.client.force_login(User.objects.first())
        resp = self.client.get(reverse('accounts:profile_change', args=[1]))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.resolver_match.func.__name__, ChangeProfileView.as_view().__name__)

        self.assertIsNotNone(resp.context['group'])
