from django.db import models
from django.conf import settings

class ProductViewEvent(models.Model):
    product = models.ForeignKey('marketplace.Product', on_delete=models.CASCADE, related_name='view_events')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self):
        return f"View for {self.product.title} at {self.timestamp}"

class DailySalesSummary(models.Model):
    date = models.DateField(unique=True)
    total_sales_usd = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_orders = models.PositiveIntegerField(default=0)
    # Storing volume in the native crypto amount, not USD equivalent
    currency_pi_volume = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    currency_sidra_volume = models.DecimalField(max_digits=20, decimal_places=8, default=0)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Daily Sales Summaries"

    def __str__(self):
        return f"Sales for {self.date}: ${self.total_sales_usd}"
