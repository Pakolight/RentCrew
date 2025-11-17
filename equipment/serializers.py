from django.utils.text import slugify
from rest_framework import serializers
from equipment.models import CatalogItem

class CatalogItemSerializer(serializers.ModelSerializer):
    sku = serializers.CharField(read_only=True)

    def _generate_sku(self, name: str, model: str | None) -> str:
        base_slug = slugify("-".join(filter(None, [name, model])))
        return base_slug or slugify(name)

    def create(self, validated_data):
        name = validated_data.get("name", "")
        model = validated_data.get("model")
        validated_data["sku"] = self._generate_sku(name, model)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        name = validated_data.get("name", instance.name)
        model = validated_data.get("model", instance.model)
        validated_data["sku"] = self._generate_sku(name, model)
        return super().update(instance, validated_data)

    class Meta:
        model = CatalogItem
        fields = [
            'id', 'sku', 'name', 'category', 'subcategory', 'brand', 'model',
            'sellable', 'rentable', 'isConsumable', 'defaultRate', 'pricePolicy',
            'weight', 'power', 'dimensions', 'upright_only', 'image', 'company'
        ]