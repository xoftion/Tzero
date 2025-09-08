from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from ..forms import UserRegistrationForm, UserLoginForm

class RegistrationView(SuccessMessageMixin, CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    success_message = "Your account has been created successfully! You can now log in."

class LoginView(SuccessMessageMixin, auth_views.LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('users:dashboard')
    success_message = "You have been successfully logged in."

class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    next_page = reverse_lazy('core:home')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have been successfully logged out.")
        return super().dispatch(request, *args, **kwargs)

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'users/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_seller'] = self.request.user.is_seller
        return context

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'
