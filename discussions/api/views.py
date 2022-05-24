from rest_framework import generics, permissions
from django.contrib.auth.models import User

from accounts.models import Profile
from .serializers import DiscussionsSerializer
from discussions.models import Discussions


class ListDiscussionView(generics.ListAPIView):
    serializer_class = DiscussionsSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        return Discussions.objects.filter(
            created_user__in=(
                User.objects.filter(profile__in=Profile.objects.filter(group__profile__user=self.request.user).all())
            ),
            is_general_discussions=False
        ).order_by('change_date').all()
