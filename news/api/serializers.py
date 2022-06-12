from abc import ABC

from rest_framework import serializers

from news.models import Tag, NewsModel, TagUserChoice


class TagSerializers(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)

    class Meta:
        model = Tag
        fields = ('id', 'name')


class UpdateNewsTagSerializers(serializers.ModelSerializer):

    class Meta:
        model = NewsModel
        fields = ('tags', )

    def update(self, instance, validated_data):
        instance.tags.add(validated_data['tags'][0])
        return instance


class TagUserChoiceSerializers(serializers.ModelSerializer):

    class Meta:
        model = TagUserChoice
        fields = ('tag', 'choice')


class ListNewsSerializers(serializers.ModelSerializer):

    class Meta:
        model = NewsModel
        fields = ('id', 'title', )


class CreateNewsSerializers(serializers.ModelSerializer):

    class Meta:
        model = NewsModel
        fields = ('title', 'body')


class NewsSerializers(serializers.ModelSerializer):

    class Meta:
        model = NewsModel
        fields = ('title', 'body', 'tags')
