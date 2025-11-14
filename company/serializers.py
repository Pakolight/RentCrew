from rest_framework import serializers
from django.contrib.auth import authenticate


class CompanySerializer (serializers.Serializer):
    legalName = serializers.CharField(max_length=255)
    tradeName = serializers.CharField(max_length=255)
    vatNumber = serializers.CharField(max_length=50)
    iban = serializers.CharField(max_length=50)
    address = serializers.CharField(max_length=255)

class SessionLoginSerializer(serializers.Serializer):
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
