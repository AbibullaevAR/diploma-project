from django.test import TestCase

from news.models import Tag, NewsModel


class TagModelTest(TestCase):

    @classmethod
    def create_tag(cls, tag_name, group):
        tag = Tag.objects.create(
            name=tag_name,
            group=group
        )
        tag.save()
        return tag


class NewsModelTest(TestCase):

    @classmethod
    def create_news(cls, user, title, body, tags):
        created_news = NewsModel.objects.create(
            created_user=user,
            title=title,
            body=body
        )
        if tags:
            created_news.tags.add(tags)

        return created_news
