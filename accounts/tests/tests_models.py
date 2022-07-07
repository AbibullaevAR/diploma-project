from django.test import TestCase
from django.contrib.auth.models import User

from accounts.models import Group, Profile


class UserModelTest(TestCase):

    @classmethod
    def create_user(
            cls,
            username='test_user_name',
            email='test_email@mail.ru',
            first_name='test_first_name',
            last_name='test_last_name',
            password='test_password'
    ):
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        return user

    @classmethod
    def setUpTestData(cls):

        users_data = {
            'username': 'test_user_name{}',
            'email': 'test_email{}@mail.ru',
            'first_name': 'test_first_name{}',
            'last_name': 'test_last_name{}',
            'password': 'test_password{}'
        }

        created_users = [cls.create_user(
            **{key: value.format(i) for key, value in users_data.items()}
        ) for i in range(3)]

        group = GroupModelTest.create_group(group_name='test_group_name')
        [ProfileModelTest.create_profile(user, group) for user in created_users]

    def test_get_group_for_user(self):
        self.assertEqual(User.objects.first().profile_set.first().group.group_name, 'test_group_name')

    def test_get_all_users_in_group(self):
        self.assertQuerysetEqual(
            User.objects.filter(
                profile__in=Profile.objects.filter(group__profile__user=User.objects.first()).all()
            ).all(),
            User.objects.all(),
            ordered=False
        )


class GroupModelTest(TestCase):

    @classmethod
    def create_group(cls, group_name='test_group_name'):
        return Group.objects.create(
            group_name=group_name
        )

    @classmethod
    def setUpTestData(cls):
        cls.create_group('test_group_name1')


class ProfileModelTest(TestCase):

    @classmethod
    def create_profile(cls, user, group):
        return Profile.objects.create(
            user=user,
            group=group
        )

    @classmethod
    def setUpTestData(cls):
        pass
























