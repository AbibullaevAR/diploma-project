from rest_framework import serializers

from attached_file.models import UserFiles


class CreateUserFileSerializer(serializers.ModelSerializer):

    discussion_id = serializers.IntegerField(required=True)

    class Meta:
        model = UserFiles
        fields = ('file_name', 'discussion_id')
