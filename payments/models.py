from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Wallet(models.Model):
    class Currency(models.TextChoices):
        PI = "PI", _("Pi")
        SIDRA = "SIDRA", _("Sidra")

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wallets')
    currency = models.CharField(max_length=5, choices=Currency.choices)
    address = models.CharField(max_length=42, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'currency')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s {self.get_currency_display()} Wallet"
