from django.contrib.auth import get_user_model
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from company.serializers import JWTLoginSerializer, CompanySerializer, UserSerializer


from company.models import Company


User = get_user_model()


def _serialize_user(user: User) -> dict:
    return {
        'id': user.pk,
        'email': user.email,
        'firstName': user.first_name,
        'lastName': user.last_name,
        'role': getattr(user, 'role', None),
        'companyId': user.company_id,
    }

class CompanyCreateAPIView(CreateAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        company = serializer.save()
        user = User.objects.filter(id=self.request.data['owner']).first()
        user.company = company
        user.save()



class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]




class JWTTokenObtainView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = JWTLoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        # Return user data and tokens
        data = {
            'user': _serialize_user(user),
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }

        return Response(data, status=status.HTTP_200_OK)


class JWTTokenStatusView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        is_authenticated = request.user.is_authenticated
        payload = {
            'isAuthenticated': is_authenticated,
        }
        if is_authenticated:
            payload['user'] = _serialize_user(request.user)
        return Response(payload, status=status.HTTP_200_OK)


class JWTTokenBlacklistView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        response_data = {'detail': 'No action taken'}

        # Handle JWT logout
        refresh_token = request.data.get('refresh')
        if refresh_token:
            try:
                # Blacklist the refresh token
                token = RefreshToken(refresh_token)
                token.blacklist()
                response_data = {'detail': 'JWT logout successful'}
                return Response(response_data, status=status.HTTP_200_OK)
            except Exception as e:
                response_data = {'detail': str(e)}
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
