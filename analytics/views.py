from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import DailySalesSummary

class SalesAnalyticsDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # We'll fetch the last 30 days of data for the chart
        thirty_days_ago = timezone.now().date() - timedelta(days=30)
        summaries = DailySalesSummary.objects.filter(date__gte=thirty_days_ago).order_by('date')

        # Format data for Chart.js
        context['chart_labels'] = [s.date.strftime('%b %d') for s in summaries]
        context['chart_data_sales'] = [float(s.total_sales_usd) for s in summaries]
        context['chart_data_orders'] = [s.total_orders for s in summaries]

        context['total_sales_30_days'] = sum(s.total_sales_usd for s in summaries)
        context['total_orders_30_days'] = sum(s.total_orders for s in summaries)

        return context
