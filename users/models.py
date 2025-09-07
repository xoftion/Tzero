from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class Role(models.TextChoices):
        BUYER = "BUYER", _("Buyer")
        SELLER = "SELLER", _("Seller")
        ADMIN = "ADMIN", _("Admin")

    class KYCStatus(models.TextChoices):
        UNVERIFIED = "UNVERIFIED", _("Unverified")
        PENDING = "PENDING", _("Pending")
        VERIFIED = "VERIFIED", _("Verified")
        REJECTED = "REJECTED", _("Rejected")

    # The default 'email' field in AbstractUser is not unique.
    # We make it unique for registration and password reset purposes.
    email = models.EmailField(_("email address"), unique=True)

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.BUYER)

    # Using ImageField for now. Cloudinary integration will handle the storage.
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    reputation = models.FloatField(default=5.0, help_text="User's reputation score from 0.0 to 5.0")

    kyc_status = models.CharField(max_length=15, choices=KYCStatus.choices, default=KYCStatus.UNVERIFIED)

    two_factor_enabled = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    @property
    def is_seller(self):
        return self.role in (self.Role.SELLER, self.Role.ADMIN)

    @property
    def is_buyer(self):
        return self.role in (self.Role.BUYER, self.Role.ADMIN)

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN
