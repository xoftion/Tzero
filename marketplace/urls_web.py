from django.urls import path
from .views import web as views

app_name = 'marketplace'

urlpatterns = [
    # Public views
    path('', views.ProductListView.as_view(), name='product_list'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),

    # Seller views
    path('my-products/', views.SellerProductListView.as_view(), name='seller_product_list'),
    path('my-products/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('my-products/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('my-products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
]
