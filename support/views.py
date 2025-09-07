from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import SupportTicket
from .forms import TicketForm, MessageForm

class TicketListView(LoginRequiredMixin, ListView):
    model = SupportTicket
    template_name = 'support/ticket_list.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        return SupportTicket.objects.filter(user=self.request.user)

class TicketDetailView(LoginRequiredMixin, DetailView):
    model = SupportTicket
    template_name = 'support/ticket_detail.html'
    context_object_name = 'ticket'

    def get_queryset(self):
        return SupportTicket.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message_form'] = MessageForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.ticket = self.object
            message.user = request.user
            message.save()
            return HttpResponseRedirect(self.object.get_absolute_url()) # Assuming get_absolute_url is defined

        context = self.get_context_data()
        context['message_form'] = form
        return self.render_to_response(context)

class TicketCreateView(LoginRequiredMixin, CreateView):
    model = SupportTicket
    form_class = TicketForm
    template_name = 'support/ticket_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('support:ticket_detail', kwargs={'pk': self.object.pk})
