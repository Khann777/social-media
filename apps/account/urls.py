from django.urls import path, include
from knox.views import LogoutAllView
from apps.account.views import LogoutView
from .views import RegisterView, LoginView, ResetPasswordView, PasswordResetConfirmView ,ActivateView, ProfileAll, ProfileDetailView

app_name = 'account'

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('activate/', ActivateView.as_view()),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout_all/', LogoutAllView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),
    path('reset-password-confirm/', PasswordResetConfirmView.as_view()),
    path('profile/', ProfileAll.as_view()),
    path('profile/<int:pk>/', ProfileDetailView.as_view()),

]