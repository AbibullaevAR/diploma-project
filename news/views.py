from django.shortcuts import render
from django.views.generic.edit import FormView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import Profile
from .models import Tag, NewsModel
from .forms import CreateNewsForm


# Create your views here.


class CreateNewsView(LoginRequiredMixin, FormView):
    template_name = 'news/create_news.html'
    form_class = CreateNewsForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['tags'] = self.get_tags_filter_group()
        return context

    def form_valid(self, form):
        create_news = form.save(commit=False)
        # Get group for requested user
        group = Profile.objects.filter(user=self.request.user).first().group

        tags_s = str(form.cleaned_data['tags']).split('#')[1:]

        tags_from_db = self.get_tags_filter_group()

        # Check equals name tag
        # if tag not exist in db, create obj
        tags_not_db = [Tag(name=item, group=group) for item in tags_s if item not in [x.name for x in tags_from_db]]

        # Save creating obj in db
        [item.save() for item in tags_not_db]

        create_news.created_user = self.request.user

        # Save model before create relationship m2m
        create_news.save()

        create_news.tags.add(*tags_not_db)
        create_news.tags.add(*tags_from_db)

        create_news.save()

        return super(CreateNewsView, self).form_valid(form)

    def get_tags_filter_group(self):
        # Subquery find Profile for user
        # user do not have relationship with Group
        return Tag.objects.filter(
            group=Profile.objects.filter(user=self.request.user).first().group
        ).all()


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
