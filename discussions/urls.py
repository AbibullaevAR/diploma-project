from django.urls import path, include

from .views import CreateDiscussionView, UpdateDiscussionView, DetailDiscussionView, DelateDiscussionView

app_name = 'discussions'
urlpatterns = [
    path('create_discussion/', CreateDiscussionView.as_view(), name='create_discussion'),
    path('update_discussion/<int:pk>', UpdateDiscussionView.as_view(), name='update_discussion'),
    path('detail_discussion/<int:pk>', DetailDiscussionView.as_view(), name='detail_discussion'),
    path('delate_discussion/<int:pk>', DelateDiscussionView.as_view(), name='delate_discussion')
]
