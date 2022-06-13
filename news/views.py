from django.shortcuts import render, reverse
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import Profile
from .models import Tag, NewsModel
from .forms import CreateNewsForm


# Create your views here.

class CreateNewsView(LoginRequiredMixin, CreateView):
    model = NewsModel
    fields = ('title', 'body')
    template_name = 'news/create_news.html'
    success_url = reverse('diplomaProject:main_page')

    def get_context_data(self, **kwargs):
        contex = super(CreateNewsView, self).get_context_data(**kwargs)
        contex['tags'] = Tag.objects.filter(group__profile__user=self.request.user).all()
        return contex


class UpdateNewsView(LoginRequiredMixin, UpdateView):
    model = NewsModel
    fields = ('title', 'body')
    template_name = 'news/update_news.html'
    success_url = reverse('diplomaProject:main_page')


class ListChoiceView(LoginRequiredMixin, ListView):
    template_name = 'news/list_choice.html'
    context_object_name = 'tags'

    def get_queryset(self):
        return Tag.objects.filter(group__profile__user=self.request.user)


class NewsDetailView(LoginRequiredMixin, DetailView):
    template_name = 'news/detail_news.html'
    model = NewsModel
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        contex = super(NewsDetailView, self).get_context_data(**kwargs)
        contex['tags'] = Tag.objects.filter(group__profile__user=self.request.user).all()
        contex['news_tags'] = self.object.tags.all()
        return contex
