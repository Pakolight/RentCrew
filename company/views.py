from django.contrib.auth import authenticate, get_user_model, login, logout
from django.middleware import csrf
from rest_framework import serializers, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from company.serializers import SessionLoginSerializer, CompanySerializer, UserSerializer


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


class SessionCSRFCookieView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        token = csrf.get_token(request)
        return Response({'csrfToken': token})


class SessionLoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = SessionLoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        login(request, user)
        token = csrf.get_token(request)
        data = {
            'user': _serialize_user(user),
            'csrfToken': token,
        }
        return Response(data, status=status.HTTP_200_OK)


class SessionStatusView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [SessionAuthentication]

    def get(self, request):
        is_authenticated = request.user.is_authenticated
        payload = {
            'isAuthenticated': is_authenticated,
            'csrfToken': csrf.get_token(request),
        }
        if is_authenticated:
            payload['user'] = _serialize_user(request.user)
        return Response(payload, status=status.HTTP_200_OK)


class SessionLogoutView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [SessionAuthentication]

    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
        token = csrf.get_token(request)
        return Response({'detail': 'Logged out', 'csrfToken': token}, status=status.HTTP_200_OK)
