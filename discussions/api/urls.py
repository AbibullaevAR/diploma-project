from django.urls import path

from .views import ListDiscussionView

app_name = 'api'
urlpatterns = [
    path('list_discussion/', ListDiscussionView.as_view(), name='list_discussions')
]
