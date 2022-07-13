from django.test import TestCase
from django.contrib.auth.models import User

from accounts.forms import MentorRegistrationForm
from accounts.models import Group, Profile


class MentorRegistrationFormTest(TestCase):

    def setUp(self):
        self.form = MentorRegistrationForm(data={
            'email': 'test_email@mail.ru',
            'group': 'test_group_name'
        })

    def test_valid_form(self):
        self.assertTrue(self.form.is_valid())
        self.form.save(commit=True)

        created_user = User.objects.first()

        self.assertEqual(created_user.email, 'test_email@mail.ru')
        self.assertEqual(created_user.username, 'test_email@mail.ru')
        self.assertTrue(created_user.has_perm('accounts.mentor'))

        created_profile = Profile.objects.first()

        self.assertTrue(isinstance(created_profile, Profile))
        self.assertEqual(created_profile.group.group_name, 'test_group_name')
        self.assertEqual(created_profile.user, created_user)
