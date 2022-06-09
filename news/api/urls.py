from django.urls import path

from .views import TagList, UpdateNewsTagView, CreateTagUserChoiceView, UpdateTagUserChoiceView, ListNewsView, CreateNewsView
app_name = 'api'
urlpatterns = [
    path('tags/', TagList.as_view(), name='tags'),
    path('update_news_tag/', UpdateNewsTagView.as_view(), name='update_news_tag'),
    path('create_choice/', CreateTagUserChoiceView.as_view(), name='create_choice'),
    path('update_choice/', UpdateTagUserChoiceView.as_view(), name='update_choice'),
    path('list_news/', ListNewsView.as_view(), name='list_news'),
    path('create_news/', CreateNewsView.as_view(), name='create_news')
]
