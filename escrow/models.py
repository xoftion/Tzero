from django.db import models
from django.utils.translation import gettext_lazy as _

class Escrow(models.Model):
    class EscrowState(models.TextChoices):
        CREATED = "CREATED", _("Created")
        FUNDED = "FUNDED", _("Funded")
        RELEASED = "RELEASED", _("Released")
        REFUNDED = "REFUNDED", _("Refunded")
        IN_DISPUTE = "IN_DISPUTE", _("In Dispute")

    # This will be the bytes32 dealId from the smart contract
    deal_id = models.CharField(max_length=66, unique=True, primary_key=True)

    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE, related_name='escrow', null=True)

    status = models.CharField(max_length=15, choices=EscrowState.choices, default=EscrowState.CREATED)

    funding_tx_hash = models.CharField(max_length=66, blank=True, null=True)
    release_tx_hash = models.CharField(max_length=66, blank=True, null=True)
    refund_tx_hash = models.CharField(max_length=66, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Escrow {self.deal_id[:10]}... - {self.get_status_display()}"
