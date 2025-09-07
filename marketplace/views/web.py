from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.conf import settings
from decimal import Decimal
from ..models import Product
from ..forms import ProductForm
from ..mixins import SellerRequiredMixin

class ProductListView(ListView):
    model = Product
    template_name = 'marketplace/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        return Product.objects.filter(is_active=True).order_by('-created_at')

class ProductDetailView(DetailView):
    model = Product
    template_name = 'marketplace/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Product.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        pi_rate = Decimal(getattr(settings, 'PI_USD_RATE', '0.34'))
        sidra_ngn_rate = Decimal(getattr(settings, 'SIDRA_NGN_RATE', '50'))
        ngn_usd_rate = Decimal(getattr(settings, 'NGN_USD_RATE', '0.0007'))

        if pi_rate > 0:
            context['pi_price'] = product.price_usd / pi_rate
        else:
            context['pi_price'] = 'N/A'

        if sidra_ngn_rate > 0 and ngn_usd_rate > 0:
            price_ngn = product.price_usd / ngn_usd_rate
            context['sidra_price'] = price_ngn / sidra_ngn_rate
        else:
            context['sidra_price'] = 'N/A'

        return context

class SellerProductListView(SellerRequiredMixin, ListView):
    model = Product
    template_name = 'marketplace/seller_product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user).order_by('-created_at')

class ProductCreateView(SellerRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'marketplace/product_form.html'
    success_url = reverse_lazy('marketplace:seller_product_list')

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)

class ProductUpdateView(SellerRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'marketplace/product_form.html'
    success_url = reverse_lazy('marketplace:seller_product_list')

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)

class ProductDeleteView(SellerRequiredMixin, DeleteView):
    model = Product
    template_name = 'marketplace/product_confirm_delete.html'
    success_url = reverse_lazy('marketplace:seller_product_list')

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)
