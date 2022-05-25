from rest_framework import serializers

from discussions.models import Discussions


class DiscussionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Discussions
        fields = ('name', 'change_date')

