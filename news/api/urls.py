from django.urls import path

from .views import TagList, UpdateNewsTagView, UpdateTagUserChoiceView, UpdateNewsView
app_name = 'api'
urlpatterns = [
    path('tags/', TagList.as_view(), name='tags'),
    path('update_news_tag/', UpdateNewsTagView.as_view(), name='update_news_tag'),
    path('update_choice/', UpdateTagUserChoiceView.as_view(), name='update_choice'),
    path('update_news/', UpdateNewsView.as_view(), name='update_news')
]
