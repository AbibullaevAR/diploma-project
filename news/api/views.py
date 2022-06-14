from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics
from rest_framework import permissions

from accounts.models import Profile
from news.models import Tag, NewsModel, TagUserChoice
from .serializers import TagSerializers, UpdateNewsTagSerializers, TagUserChoiceSerializers, ListNewsSerializers,\
CreateNewsSerializers, NewsSerializers


class TagList(generics.ListCreateAPIView):
    serializer_class = TagSerializers
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):

        if pk := self.request.query_params.get('pk', None):
            return NewsModel.objects.filter(id=pk).first().tags.all()

        return Tag.objects.filter(group=self.get_group_current_user()).all()

    def perform_create(self, serializer):
        self.created_instance = serializer.save(group=self.get_group_current_user())

    def get_group_current_user(self):
        """
        Return group obj for current auth user.
        :return: Group model obj
        """
        return Profile.objects.filter(user=self.request.user).first().group

    def get_success_headers(self, data):
        headers = super().get_success_headers(data)
        headers['create_obj_pk'] = self.created_instance.pk
        return headers


class UpdateNewsTagView(generics.UpdateAPIView):

    serializer_class = UpdateNewsTagSerializers
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        return NewsModel.objects.filter(id=self.request.query_params['pk']).first()


class CreateTagUserChoiceView(generics.CreateAPIView):
    serializer_class = TagUserChoiceSerializers
    permission_classes = [permissions.IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UpdateTagUserChoiceView(generics.UpdateAPIView):
    serializer_class = TagUserChoiceSerializers
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        if tag := TagUserChoice.objects.filter(
                tag_id=self.request.query_params.get('pk'), user=self.request.user
        ).first():
            return tag
        return TagUserChoice(user=self.request.user)


class ListNewsView(generics.ListAPIView):
    serializer_class = ListNewsSerializers
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        return NewsModel.objects.filter(
            ~Q(tags__in=
                [item.tag for item in TagUserChoice.objects.filter(user=self.request.user, choice=False).all()]
               ),
            created_user__in=(
                User.objects.filter(profile__in=Profile.objects.filter(group__profile__user=self.request.user).all())
            )
        ).all().order_by('-change_date')


class CreateNewsView(generics.CreateAPIView):
    serializer_class = CreateNewsSerializers
    permission_classes = [permissions.IsAuthenticated, ]

    def perform_create(self, serializer):
        self.created_instance = serializer.save(created_user=self.request.user)

    def get_success_headers(self, data):
        headers = super().get_success_headers(data)
        headers['create_obj_pk'] = self.created_instance.pk
        return headers


class UpdateNewsView(generics.UpdateAPIView):
    serializer_class = NewsSerializers
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        if news := NewsModel.objects.filter(pk=self.request.query_params.get('pk')).first():
            return news
        return NewsModel(created_user=self.request.user)
