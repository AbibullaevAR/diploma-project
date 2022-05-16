from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
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


class PswResetView(PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')


