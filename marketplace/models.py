from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    class ProductType(models.TextChoices):
        DIGITAL = "DIGITAL", _("Digital")
        PHYSICAL = "PHYSICAL", _("Physical")

    class CurrencyPreference(models.TextChoices):
        PI = "PI", _("Pi")
        SIDRA = "SIDRA", _("Sidra")

    product_type = models.CharField(max_length=10, choices=ProductType.choices)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    tags = models.ManyToManyField(Tag, blank=True, related_name='products')

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()

    price_usd = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in USD")
    currency_preference = models.CharField(max_length=5, choices=CurrencyPreference.choices, default=CurrencyPreference.PI)

    digital_file = models.FileField(upload_to='digital_products/', null=True, blank=True, help_text="Required for digital products")

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure slug is unique
            qs = Product.objects.filter(slug=self.slug)
            if qs.exists():
                self.slug = f"{self.slug}-{self.id}"
        super().save(*args, **kwargs)

    def clean(self):
        if self.product_type == self.ProductType.DIGITAL and not self.digital_file:
            raise models.ValidationError(_("A file must be uploaded for digital products."))
        if self.product_type == self.ProductType.PHYSICAL and self.digital_file:
            self.digital_file = None

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('marketplace:product_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.product.title}"

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='reviews', null=True)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('order', 'user') # A user can only review an order once
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.title}"
