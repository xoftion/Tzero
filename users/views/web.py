from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, View, UpdateView
from django.contrib.auth import views as auth_views, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from ..forms import UserRegistrationForm, UserLoginForm, UserUpdateForm

User = get_user_model()

# ... (rest of the file is the same until ProfileView)

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return ( str(user.pk) + str(timestamp) + str(user.is_active) )
account_activation_token = AccountActivationTokenGenerator()

class RegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:verification_sent')
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        activation_link = self.request.build_absolute_uri(reverse_lazy('users:activate', kwargs={'uidb64': uid, 'token': token}))
        subject = "Activate Your UltrokPay Account"
        message = render_to_string('users/verification_email.html', {'user': user, 'activation_link': activation_link})
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        return super().form_valid(form)

class VerificationEmailSentView(TemplateView):
    template_name = 'users/verification_sent.html'

class ActivateAccountView(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Your account has been successfully activated. You can now log in.")
            return redirect('users:login')
        else:
            return render(request, 'users/verification_invalid.html')

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

class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Your profile has been updated successfully.')
        return super().form_valid(form)

class PasswordChangeView(SuccessMessageMixin, auth_views.PasswordChangeView):
    template_name = 'users/password_change_form.html'
    success_url = reverse_lazy('users:profile')
    success_message = "Your password was updated successfully."
