from celery import shared_task
from django.utils import timezone
from datetime import date, timedelta
from django.db.models import Sum, Count

from orders.models import Order
from .models import DailySalesSummary

@shared_task
def process_daily_sales():
    """
    A Celery task to calculate and save the sales summary for the previous day.
    This should be scheduled to run once a day, shortly after midnight.
    """
    yesterday = date.today() - timedelta(days=1)

    # Get all orders that were created yesterday
    orders_yesterday = Order.objects.filter(created_at__date=yesterday, status='PAID') # Assuming 'PAID' is a final status

    if not orders_yesterday.exists():
        # Create a summary with zero values if no sales
        DailySalesSummary.objects.get_or_create(
            date=yesterday,
            defaults={
                'total_sales_usd': 0,
                'total_orders': 0,
            }
        )
        return f"No sales recorded for {yesterday}."

    # Aggregate the data
    summary_data = orders_yesterday.aggregate(
        total_sales=Sum('total_price_usd'),
        total_orders=Count('id')
    )

    # Note: Calculating crypto volume would require storing the currency and amount
    # paid for each order. This is not currently in the Order model.
    # This is a placeholder for that logic.
    pi_volume = 0
    sidra_volume = 0

    # Create or update the summary for that day
    summary, created = DailySalesSummary.objects.update_or_create(
        date=yesterday,
        defaults={
            'total_sales_usd': summary_data['total_sales'] or 0,
            'total_orders': summary_data['total_orders'] or 0,
            'currency_pi_volume': pi_volume,
            'currency_sidra_volume': sidra_volume,
        }
    )

    if created:
        return f"Created daily sales summary for {yesterday}."
    else:
        return f"Updated daily sales summary for {yesterday}."
