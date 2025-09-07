from django import forms
from .models import SupportTicket, TicketMessage

class TicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ['title', 'order', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit the order choices to the user's own orders
        if user:
            self.fields['order'].queryset = user.orders.all()

class MessageForm(forms.ModelForm):
    class Meta:
        model = TicketMessage
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Type your reply...'}),
        }
        labels = {
            'message': ''
        }
