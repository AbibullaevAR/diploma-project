from django.contrib.auth.models import User
from django.test import TestCase

from accounts.tests.tests_models import UserModelTest
from discussions.models import Discussions, Message


class DiscussionsModelTest(TestCase):

    @classmethod
    def create_discussion(cls, created_user, name):
        return Discussions.objects.create(
            created_user=created_user,
            name=name
        )

    @classmethod
    def setUpTestData(cls):
        UserModelTest.setUpTestData()
        cls.create_discussion(User.objects.first(), name='test_name')


class MessageModelTest(TestCase):

    @classmethod
    def create_message(cls, created_user, body, discussion):
        return Message.objects.create(
            created_user=created_user,
            body=body,
            discussion=discussion
        )
