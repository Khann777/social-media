from django.urls import path
from knox.views import LogoutView, LogoutAllView

from .views import RegisterView, LoginView, ResetPasswordView, PasswordResetConfirmView ,ActivateView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('activate/', ActivateView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('logout_all/', LogoutAllView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),
    path('reset-password-confirm/', PasswordResetConfirmView.as_view())
]