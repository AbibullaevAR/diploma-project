from django.urls import path

from .views import TagList, UpdateNewsTagView
app_name = 'api'
urlpatterns = [
    path('tags/', TagList.as_view(), name='tags'),
    path('update_news_tag/', UpdateNewsTagView.as_view(), name='update_news_tag'),
]
