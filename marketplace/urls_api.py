from django.urls import path
from .views import api as api_views

urlpatterns = [
    path('products/', api_views.ProductListAPIView.as_view(), name='product-list'),
    path('products/create/', api_views.ProductCreateAPIView.as_view(), name='product-create'),
    path('products/<slug:slug>/', api_views.ProductDetailAPIView.as_view(), name='product-detail'),
    path('products/<slug:slug>/update/', api_views.ProductUpdateAPIView.as_view(), name='product-update'),
    path('products/<slug:slug>/delete/', api_views.ProductDestroyAPIView.as_view(), name='product-delete'),
]
