from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from users.serializers import UserRegistrationSerializer, UserSerializer

User = get_user_model()

class UserRegistrationAPIView(generics.CreateAPIView):
    """
    API view for user registration.
    Allows any user (authenticated or not) to create a new user account.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


class CurrentUserAPIView(generics.RetrieveAPIView):
    """
    API view to retrieve the authenticated user's details.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
