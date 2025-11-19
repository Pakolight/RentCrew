from rest_framework import serializers
from django.contrib.auth import authenticate

from company.models import Company, User


class CompanySerializer (serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "owner", 'legalName', 'tradeName', 'vatNumber', 'iban',  'logo', 'country', 'street_address', 'city', 'state_province', 'zip_postal_code']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'company', 'password']

class JWTLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(trim_whitespace=False, write_only=True)

    def validate(self, attrs):
        request = self.context.get('request')
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            msg = serializers.ValidationError('Both email and password are required.', code='authorization')
            raise msg

        user = authenticate(request=request, email=email, password=password)
        if user is None:
            raise serializers.ValidationError('Unable to log in with provided credentials.', code='authorization')

        if not user.is_active:
            raise serializers.ValidationError('User account is disabled.', code='authorization')

        attrs['user'] = user
        return attrs
