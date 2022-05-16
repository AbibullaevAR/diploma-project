from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic.edit import FormView, UpdateView

from .forms import MentorRegistrationForm
from .mail_util import send_complete_reg_mail


# Create your views here.
class MentorRegistrationView(FormView):
    template_name = 'accounts/MentorRegistrationTemplate.html'
    form_class = MentorRegistrationForm
    success_url = '/'

    def form_valid(self, form):
        user = form.save(True)

        send_complete_reg_mail(self.request.scheme, self.request.get_host(), user.email)

        return super(MentorRegistrationView, self).form_valid(form)


class ChangeProfileView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ('username', 'last_name', 'first_name')
    template_name = 'accounts/user_profile.html'
    success_url = '/'
