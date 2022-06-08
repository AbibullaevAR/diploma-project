from django.urls import path

from .views import CreateStudentUserView

app_name = 'api'
urlpatterns = [
    path('create_student/', CreateStudentUserView.as_view(), name='create_student'),
]
