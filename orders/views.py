from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View, DetailView, TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from .models import Cart, CartItem, Order, OrderItem
from marketplace.models import Product
from escrow.models import Escrow
from core.services import BlockchainService
import uuid

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        seller_subquery = Order.objects.filter(items__product__seller=self.request.user)
        return Order.objects.filter(
            Q(buyer=self.request.user) | Q(pk__in=seller_subquery)
        ).distinct().order_by('-created_at')

class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=self.kwargs.get('product_id'))
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 1}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect('orders:cart_detail')

class CartDetailView(LoginRequiredMixin, DetailView):
    model = Cart
    template_name = 'orders/cart_detail.html'
    context_object_name = 'cart'

    def get_object(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart

class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        item_id = self.kwargs.get('item_id')
        cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
        cart_item.delete()
        return redirect('orders:cart_detail')

class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        context['cart'] = cart
        return context

    def post(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, user=request.user)
        if not cart.items.exists():
            return redirect('orders:cart_detail')

        seller = cart.items.first().product.seller

        with transaction.atomic():
            order = Order.objects.create(
                buyer=request.user,
                total_price_usd=cart.total_price
            )
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price_at_purchase_usd=item.product.price_usd
                )

            deal_id = uuid.uuid4().bytes
            token_address = "0x0000000000000000000000000000000000000000"
            currency = cart.items.first().product.currency_preference

            Escrow.objects.create(
                deal_id=deal_id.hex(),
                order=order,
            )
            cart.items.all().delete()

        return redirect('orders:order_detail', pk=order.pk)

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        # Users can only see their own orders (either as buyer or seller)
        seller_subquery = Order.objects.filter(items__product__seller=self.request.user)
        return Order.objects.filter(
            Q(buyer=self.request.user) | Q(pk__in=seller_subquery)
        ).distinct()
