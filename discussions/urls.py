from django.urls import path, include

from .views import CreateDiscussionView, DetailDiscussionView

app_name = 'discussions'
urlpatterns = [
    path('create_discussion/', CreateDiscussionView.as_view(), name='create_discussion'),
    path('detail_discussion/<int:pk>', DetailDiscussionView.as_view(), name='detail_discussion'),
]
