from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('dashboard/', views.SalesAnalyticsDashboardView.as_view(), name='dashboard'),
]
