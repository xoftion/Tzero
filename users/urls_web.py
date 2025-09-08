from django.urls import path
from .views import web as web_views

app_name = 'users'

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', web_views.RegistrationView.as_view(), name='register'),
    path('login/', web_views.LoginView.as_view(), name='login'),
    path('logout/', web_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', web_views.DashboardView.as_view(), name='dashboard'),
    path('profile/', web_views.ProfileView.as_view(), name='profile'),
    path('password_change/', web_views.PasswordChangeView.as_view(), name='password_change'),

    # Email Verification URLs
    path('verification-sent/', web_views.VerificationEmailSentView.as_view(), name='verification_sent'),
    path('activate/<uidb64>/<token>/', web_views.ActivateAccountView.as_view(), name='activate'),

    # Password Reset URLs
    path('password_reset/',
        auth_views.PasswordResetView.as_view(template_name='users/password_reset_form.html', email_template_name='users/password_reset_email.html', subject_template_name='users/password_reset_subject.txt'),
        name='password_reset'),
    path('password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
        name='password_reset_complete'),
]
