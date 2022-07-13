from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from accounts.tests.tests_models import UserModelTest
from attached_file.models import UserFiles
from discussions.models import Discussions, Message
from discussions.tests.test_models import DiscussionsModelTest, MessageModelTest
from discussions.views import CreateDiscussionView, DetailDiscussionView


class CreateDiscussionViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        DiscussionsModelTest.setUpTestData()
        user = User.objects.first()
        discussion = Discussions.objects.first()
        UserFiles.objects.create(
            created_user=user,
            discussion=discussion,
            file_name='file1'
        )
        UserFiles.objects.create(
            created_user=user,
            discussion=DiscussionsModelTest.create_discussion(user, 'discussion2'),
            file_name='file2'
        )
        MessageModelTest.create_message(
            created_user=user,
            body='test_body',
            discussion=discussion
        )

    def test_create_discussion(self):
        Discussions.objects.all().delete()

        user = User.objects.first()
        self.client.force_login(user)
        resp = self.client.post(reverse('discussions:create_discussion'), data={'name': 'name_discussion'}, follow=True)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.resolver_match.func.__name__, CreateDiscussionView.as_view().__name__)
        self.assertEqual(len(resp.redirect_chain), 1)

        created_discussion = Discussions.objects.first()

        self.assertIsNotNone(created_discussion)
        self.assertEqual(created_discussion.name, 'name_discussion')
        self.assertEqual(created_discussion.created_user, user)

    def test_detail_discussion(self):
        user = User.objects.first()
        discussion = Discussions.objects.first()
        self.client.force_login(user)
        resp = self.client.get(reverse('discussions:detail_discussion', args=[discussion.pk]))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.resolver_match.func.__name__, DetailDiscussionView.as_view().__name__)

        self.assertQuerysetEqual(
            resp.context['attached_file'],
            UserFiles.objects.filter(discussion=discussion),
            ordered=False
        )
        self.assertQuerysetEqual(
            resp.context['messages'],
            Message.objects.filter(discussion=discussion),
            ordered=False
        )
        self.assertQuerysetEqual(
            resp.context['participants'],
            User.objects.all(),
            ordered=False
        )


