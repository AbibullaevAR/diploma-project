from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from accounts.tests.tests_models import UserModelTest
from news.models import Tag, TagUserChoice, NewsModel
from news.tests.test_models import TagModelTest, NewsModelTest
from news.views import CreateNewsView, ListChoiceView, NewsDetailView


class CreateNewsViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        UserModelTest.setUpTestData()
        user = User.objects.first()
        group = user.profile_set.first().group
        TagModelTest.create_tag('tag1', group)
        TagModelTest.create_tag('tag2', group)
        TagModelTest.create_tag('tag3', group)

    def test_get_request(self):
        self.client.force_login(User.objects.first())
        resp = self.client.get(reverse('news:create_news'))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.resolver_match.func.__name__, CreateNewsView.as_view().__name__)

        self.assertQuerysetEqual(resp.context['tags'], Tag.objects.all(), ordered=False)


class ListChoiceViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        CreateNewsViewTest.setUpTestData()
        TagUserChoice.objects.create(
            user=User.objects.first(),
            tag=Tag.objects.first(),
            choice=False
        )

    def test_get_request(self):
        self.client.force_login(User.objects.first())
        resp = self.client.get(reverse('news:choice'))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.resolver_match.func.__name__, ListChoiceView.as_view().__name__)

        self.assertQuerysetEqual(resp.context['tags_choice_false'], [Tag.objects.first()], ordered=False)


class NewsDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        CreateNewsViewTest.setUpTestData()
        NewsModelTest.create_news(User.objects.first(), 'test_title', 'test_body', Tag.objects.first())

    def test_get_request(self):
        self.client.force_login(User.objects.first())
        resp = self.client.get(reverse('news:detail_news', args=[NewsModel.objects.first().pk]))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.resolver_match.func.__name__, NewsDetailView.as_view().__name__)

        self.assertQuerysetEqual(resp.context['news_tags'], [Tag.objects.first()], ordered=False)
        self.assertQuerysetEqual(resp.context['tags'], Tag.objects.all(), ordered=False)














