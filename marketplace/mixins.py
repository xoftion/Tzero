from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied

class SellerRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is a seller."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_seller:
            raise PermissionDenied("You must be a seller to access this page.")
        return super().dispatch(request, *args, **kwargs)
