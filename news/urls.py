from django.urls import path, include
from django.views.generic.base import TemplateView

from .views import ListChoiceView, NewsDetailView, CreateNewsView

app_name = 'news'
urlpatterns = [
    path('choice/', ListChoiceView.as_view(), name='choice'),
    path('detail_news/<int:pk>', NewsDetailView.as_view(), name='detail_news'),
    path('create_news/', CreateNewsView.as_view(), name='create_news'),

    path('api/', include('news.api.urls'))
]
