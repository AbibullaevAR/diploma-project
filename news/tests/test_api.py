import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import Group
from accounts.tests.tests_models import UserModelTest
from news.api.views import TagList, UpdateTagUserChoiceView
from news.models import Tag, TagUserChoice
from news.tests.test_models import TagModelTest, NewsModelTest


class TagListTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        UserModelTest.setUpTestData()
        user = User.objects.first()
        group = user.profile_set.first().group
        TagModelTest.create_tag('tag1', group)
        TagModelTest.create_tag('tag2', group)
        TagModelTest.create_tag('tag3', group)
        NewsModelTest.create_news(User.objects.first(), 'test_title', 'test_body', Tag.objects.first())

    def test_get_request_not_pk(self):
        self.client.force_login(User.objects.first())
        resp = self.client.get(reverse('news:api:tags'))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.resolver_match.func.__name__, TagList.as_view().__name__)

        tags = Tag.objects.all()

        self.assertEqual(
            str(resp.data),
            f"[OrderedDict([('id', {tags[0].pk}), ('name', '{tags[0].name}')]), " +
            f"OrderedDict([('id', {tags[1].pk}), ('name', '{tags[1].name}')]), " +
            f"OrderedDict([('id', {tags[2].pk}), ('name', '{tags[2].name}')])]"
        )

    def test_get_request_with_pk(self):
        self.client.force_login(User.objects.first())
        resp = self.client.get(reverse('news:api:tags'), {'pk': Tag.objects.first().pk})

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.resolver_match.func.__name__, TagList.as_view().__name__)

        self.assertEqual(resp.data, [
            {
                'id': Tag.objects.first().pk,
                'name': 'tag1'
            }
        ])

    def test_create_tag(self):
        self.client.force_login(User.objects.first())
        resp = self.client.post(reverse('news:api:tags'), {'name': 'created_tag_name'})

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.resolver_match.func.__name__, TagList.as_view().__name__)

        created_tag = Tag.objects.last()

        self.assertIsNotNone(created_tag)

        self.assertEqual(created_tag.name, 'created_tag_name')
        self.assertEqual(created_tag.group.group_name, 'test_group_name')

        self.assertEqual(resp.headers['create_obj_pk'], str(Tag.objects.last().pk))


class UpdateTagUserChoiceViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        UserModelTest.create_user()
        TagModelTest.create_tag(tag_name='tag1', group=Group.objects.create(group_name='test_group_name'))

    def check_response(self, resp):
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.resolver_match.func.__name__, UpdateTagUserChoiceView.as_view().__name__)

        tag_user_choice = TagUserChoice.objects.first()

        self.assertIsNotNone(tag_user_choice)

        self.assertEqual(tag_user_choice.tag, Tag.objects.first())
        self.assertEqual(tag_user_choice.user, User.objects.first())
        self.assertTrue(tag_user_choice.choice)

    def test_create_choice(self):
        self.client.force_login(User.objects.first())
        TagUserChoice.objects.all().delete()
        resp = self.client.put(reverse('news:api:update_choice'), {'tag': Tag.objects.first().pk, 'choice': True})

        self.check_response(resp)

    def test_update_choice(self):
        user = User.objects.first()
        self.client.force_login(user)

        TagUserChoice.objects.all().delete()

        TagUserChoice.objects.create(user=user, tag=Tag.objects.first(), choice=False)

        url = f'{reverse("news:api:update_choice")}?pk={Tag.objects.first().pk}'
        resp = self.client.put(url, {'tag': Tag.objects.first().pk, 'choice': True})

        self.check_response(resp)






