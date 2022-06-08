from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetDoneView, \
    PasswordResetCompleteView

from .views import MentorRegistrationView, ChangeProfileView, PswResetView, PswResetConfirmView

app_name = 'accounts'
urlpatterns = [
    path('mentor_registration/', MentorRegistrationView.as_view(), name='mentor_registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('rest_password_start/', PswResetView.as_view(), name='rest_password_start'),
    path('password_reset_done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', PswResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),


    path('profile/<int:pk>', ChangeProfileView.as_view(), name='profile_change'),
]
