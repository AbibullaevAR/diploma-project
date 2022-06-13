from django.shortcuts import render, reverse
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User


from accounts.models import Profile
from attached_file.models import UserFiles
from .models import Discussions, Message

# Create your views here.


class CreateDiscussionView(LoginRequiredMixin, CreateView):
    model = Discussions
    fields = ('name', )
    template_name = 'discussions/create_discussion.html'
    success_url = reverse_lazy('diplomaProject:main_page')

    def form_valid(self, form):
        discussion = form.save(commit=False)
        discussion.created_user = self.request.user
        discussion.save()

        return super(CreateDiscussionView, self).form_valid(form)


class UpdateDiscussionView(LoginRequiredMixin, UpdateView):
    model = Discussions
    fields = ('name',)
    template_name = 'discussions/update_discussion.html'
    success_url = reverse_lazy('diplomaProject:main_page')


class DetailDiscussionView(LoginRequiredMixin, DetailView):
    model = Discussions
    template_name = 'discussions/detail_discussion.html'
    context_object_name = 'discussion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attached_file'] = UserFiles.objects.filter(discussion=context['discussion']).all()
        context['messages'] = Message.objects.filter(discussion=self.get_object()).all()
        context['participants'] = User.objects.filter(
            profile__in=Profile.objects.filter(group__profile__user=self.request.user).all()
        ).all()
        return context


class DelateDiscussionView(LoginRequiredMixin, DeleteView):
    model = Discussions
    template_name = 'discussions/delate_discussion.html'
    success_url = reverse_lazy('diplomaProject:main_page')

    def form_valid(self, form):
        if self.request.user != self.get_object().created_user:
            return self.handle_no_permission()

        return super(DelateDiscussionView, self).form_valid(form)

