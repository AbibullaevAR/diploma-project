from django.urls import path, include

app_name = 'attached_file'

urlpatterns = [
    path('api/', include('attached_file.api.urls'))
]
