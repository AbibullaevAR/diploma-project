from abc import ABC

from rest_framework import serializers

from news.models import Tag, NewsModel


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

