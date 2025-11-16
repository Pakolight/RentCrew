from django.urls import path

from . import views



app_name = 'company'


urlpatterns = [
    path('csrf/', views.SessionCSRFCookieView.as_view(), name='csrf'),
    path('login/', views.SessionLoginView.as_view(), name='login'),
    path('logout/', views.SessionLogoutView.as_view(), name='logout'),
    path('session/', views.SessionStatusView.as_view(), name='session'),

    path('create/user/', views.UserCreateAPIView.as_view(), name='user-create'),
    path('create/company/', views.CompanyCreateAPIView.as_view(), name='user-create'),

]