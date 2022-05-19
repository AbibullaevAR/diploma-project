from rest_framework import generics
from rest_framework.mixins import UpdateModelMixin
from rest_framework import permissions

from .serializers import TagSerializers, UpdateNewsTagSerializers
from news.models import Tag, NewsModel
from accounts.models import Profile


class TagList(generics.ListCreateAPIView):
    serializer_class = TagSerializers
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):

        if pk := self.request.query_params.get('pk', None):
            return NewsModel.objects.filter(id=pk).first().tags.all()

        return Tag.objects.filter(group=self.get_group_current_user()).all()

    def perform_create(self, serializer):
        serializer.save(group=self.get_group_current_user())

    def get_group_current_user(self):
        """
        Return group obj for current auth user.
        :return: Group model obj
        """
        return Profile.objects.filter(user=self.request.user).first().group


class UpdateNewsTagView(generics.UpdateAPIView):

    serializer_class = UpdateNewsTagSerializers
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        return NewsModel.objects.filter(id=self.request.query_params['pk']).first()
