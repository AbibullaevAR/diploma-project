from django.urls import path, include

from .views import UserFileDetailView

app_name = 'attached_file'

urlpatterns = [
    path('download_file/<int:pk>', UserFileDetailView.as_view(), name='download_file'),
    path('api/', include('attached_file.api.urls'))
]
