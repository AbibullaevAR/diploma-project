from rest_framework import generics, permissions
from django.contrib.auth.models import User

from accounts.models import Profile, Group
from accounts.mail_util import send_complete_reg_mail
from .serializers import UserSerializer


class CreateStudentUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def perform_create(self, serializer):
        created_user = serializer.save(username=serializer.validated_data['email'])

        Profile(user=created_user, group=Group.objects.filter(profile__user=self.request.user).first()).save()

        send_complete_reg_mail(self.request.scheme, self.request.get_host(), created_user.email)



