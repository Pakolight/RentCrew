from rest_framework import serializers
from equipment.models import CatalogItem

class CatalogItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogItem
        fields = [
            'id', 'sku', 'name', 'category', 'subcategory', 'brand', 'model',
            'sellable', 'rentable', 'isConsumable', 'defaultRate', 'pricePolicy',
            'weight', 'power', 'dimensions', 'upright_only', 'image', 'company'
        ]