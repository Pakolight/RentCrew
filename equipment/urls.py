from django.urls import path
from . import views

app_name = 'equipment'

urlpatterns = [
    path('catalog-items/', views.CatalogItemListCreateAPIView.as_view(), name='catalog-item-list-create'),
    path('create/catalog-item/', views.CatalogItemCreateAPIView.as_view(), name='catalog-item-create'),
    path('catalog-items/<int:pk>/', views.CatalogItemRetrieveUpdateDestroyAPIView.as_view(), name='catalog-item-detail'),
]
