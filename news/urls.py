from django.urls import path, include

from .views import UpdateNewsView, ListChoiceView, NewsDetailView

app_name = 'news'
urlpatterns = [
    path('update_news/<int:pk>', UpdateNewsView.as_view(), name='update_news'),
    path('choice/', ListChoiceView.as_view(), name='list_choice'),
    path('detail_news/<int:pk>', NewsDetailView.as_view(), name='detail_news'),

    path('api/', include('news.api.urls'))
]
