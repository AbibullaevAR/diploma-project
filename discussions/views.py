from django.shortcuts import render
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin


from attached_file.models import UserFiles
from .models import Discussions

# Create your views here.


class CreateDiscussionView(LoginRequiredMixin, CreateView):
    model = Discussions
    fields = ('name', )
    template_name = 'discussions/create_discussion.html'
    success_url = '/'

    def form_valid(self, form):
        discussion = form.save(commit=False)
        discussion.created_user = self.request.user
        discussion.save()

        return super(CreateDiscussionView, self).form_valid(form)


class UpdateDiscussionView(LoginRequiredMixin, UpdateView):
    model = Discussions
    fields = ('name',)
    template_name = 'discussions/update_discussion.html'
    success_url = '/'


class DetailDiscussionView(LoginRequiredMixin, DetailView):
    model = Discussions
    template_name = 'discussions/detail_discussion.html'
    context_object_name = 'discussion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attached_file'] = UserFiles.objects.filter(discussion=context['discussion']).all()
        return context


class DelateDiscussionView(LoginRequiredMixin, DeleteView):
    model = Discussions
    template_name = 'discussions/delate_discussion.html'
    success_url = '/'

    def form_valid(self, form):
        if self.request.user != self.get_object().created_user:
            return self.handle_no_permission()

        return super(DelateDiscussionView, self).form_valid(form)

