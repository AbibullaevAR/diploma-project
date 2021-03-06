from django.db.models import Q
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from accounts.models import Profile
from discussions.models import Discussions
from news.models import NewsModel, TagUserChoice


class MainPageView(LoginRequiredMixin, TemplateView):
    template_name = 'diplomaProject/main_page.html'

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)

        context['discussions'] = Discussions.objects.filter(
            created_user__in=(
                User.objects.filter(profile__in=Profile.objects.filter(group__profile__user=self.request.user).all())
            ),
            is_general_discussions=False
        ).order_by('-change_date').all()

        context['news'] = NewsModel.objects.filter(
            ~Q(tags__in=
                [item.tag for item in TagUserChoice.objects.filter(user=self.request.user, choice=False).all()]
               ),
            created_user__in=(
                User.objects.filter(profile__in=Profile.objects.filter(group__profile__user=self.request.user).all())
            )
        ).all().order_by('-change_date')

        context['members'] = User.objects.filter(
            profile__in=Profile.objects.filter(group__profile__user=self.request.user).all()
        )
        context['is_mentor'] = self.request.user.has_perm('accounts.mentor')
        return context
