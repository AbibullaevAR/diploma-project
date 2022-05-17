from django.urls import path

from .views import CreateNews

app_name = 'news'
urlpatterns = [
    path('create_news/', CreateNews.as_view(), name='create_news'),
]
