from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.CartDetailView.as_view(), name='cart_detail'),
    path('history/', views.OrderListView.as_view(), name='order_list'),
    path('add/<int:product_id>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('remove/<int:item_id>/', views.RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
]
