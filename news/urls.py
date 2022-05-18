from django.urls import path

from .views import CreateNewsView, UpdateNewsView

app_name = 'news'
urlpatterns = [
    path('create_news/', CreateNewsView.as_view(), name='create_news'),
    path('update_news/<int:pk>', UpdateNewsView.as_view(), name='update_news')
]
