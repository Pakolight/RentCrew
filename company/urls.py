from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView,
)

from . import views



app_name = 'company'


urlpatterns = [
    # JWT authentication
    path('login/', views.JWTTokenObtainView.as_view(), name='login'),
    path('logout/', views.JWTTokenBlacklistView.as_view(), name='logout'),
    path('session/', views.JWTTokenStatusView.as_view(), name='session'),

    # JWT token endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),

    # User and company creation
    path('create/user/', views.UserCreateAPIView.as_view(), name='user-create'),
    path('create/company/', views.CompanyCreateAPIView.as_view(), name='company-create'),
]
