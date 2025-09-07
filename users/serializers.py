from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role')
        extra_kwargs = {
            'role': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model, used for retrieving user details.
    """
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'role',
            'profile_picture',
            'reputation',
            'kyc_status',
            'two_factor_enabled',
            'date_joined'
        )
        read_only_fields = ('date_joined', 'reputation', 'kyc_status')
