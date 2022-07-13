from django.urls import path

from .views import MainPageView
app_name = 'diplomaProject'
urlpatterns = [
    path('main_page/', MainPageView.as_view(), name='main_page')
]
