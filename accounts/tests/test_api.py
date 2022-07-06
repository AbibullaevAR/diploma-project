from django.core import mail
from django.test import TestCase
from django.contrib.auth.models import User, Permission
from django.urls import reverse

from accounts.tests.tests_models import UserModelTest
from accounts.api.views import CreateStudentUserView


class CreateStudentUserViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        UserModelTest.setUpTestData()
        permission = Permission.objects.get(codename='mentor')
        User.objects.first().user_permissions.add(permission)

    def test_create_student(self):
        self.client.force_login(User.objects.first())
        resp = self.client.post(
            reverse('accounts:api:create_student'),
            data={
                'email': 'test_student@mail.ru'
            },
            content_type='application/json'
        )

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.resolver_match.func.__name__, CreateStudentUserView.as_view().__name__)

        created_user = User.objects.filter(username='test_student@mail.ru').first()

        self.assertEqual(created_user.email, 'test_student@mail.ru')
        self.assertEqual(created_user.username, 'test_student@mail.ru')

        created_profile = created_user.profile_set.first()

        self.assertIsNotNone(created_profile)
        self.assertEqual(created_profile.group.group_name, 'test_group_name')

        self.assertEqual(len(mail.outbox), 1)

