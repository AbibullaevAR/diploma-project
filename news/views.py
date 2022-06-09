from django.shortcuts import render
from django.views.generic.edit import FormView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import Profile
from .models import Tag, NewsModel
from .forms import CreateNewsForm


# Create your views here.



class UpdateNewsView(LoginRequiredMixin, UpdateView):
    model = NewsModel
    fields = ('title', 'body')
    template_name = 'news/update_news.html'
    success_url = '/'


class ListChoiceView(ListView):
    template_name = 'news/list_choice.html'
    context_object_name = 'tags'

    def get_queryset(self):
        return Tag.objects.filter(group__profile__user=self.request.user)


class NewsDetailView(LoginRequiredMixin, DetailView):
    template_name = 'news/detail_news.html'
    model = NewsModel
    context_object_name = 'news'
