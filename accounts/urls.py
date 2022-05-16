from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView

from .views import MentorRegistrationView, ChangeProfileView

app_name = 'accounts'
urlpatterns = [
    path('mentor_registration/', MentorRegistrationView.as_view(), name='mentor_registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('rest_password_start/', PasswordResetView.as_view(), name='rest_password_start'),

    path('profile/<int:pk>', ChangeProfileView.as_view(), name='profile_change'),
]
