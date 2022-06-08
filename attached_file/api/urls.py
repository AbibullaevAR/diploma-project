from django.urls import path

from .views import CreateUserFileView


app_name = 'api'
urlpatterns = [
    path('metaINF_file/', CreateUserFileView.as_view(), name='metaINF_file'),
]
