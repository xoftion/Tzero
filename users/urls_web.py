from django.urls import path
from .views import web as web_views

app_name = 'users'

urlpatterns = [
    path('register/', web_views.RegistrationView.as_view(), name='register'),
    path('login/', web_views.LoginView.as_view(), name='login'),
    path('logout/', web_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', web_views.DashboardView.as_view(), name='dashboard'),
    path('profile/', web_views.ProfileView.as_view(), name='profile'),
]
