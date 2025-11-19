from django.contrib import admin
from .models import CatalogItem, Asset, Kit, KitItem, Case, StockLocation, Barcode

@admin.register(CatalogItem)
class CatalogItemAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'category', 'brand', 'model', 'defaultRate', 'rentable', 'sellable', 'company')
    list_filter = ('category', 'subcategory', 'brand', 'rentable', 'sellable', 'isConsumable', 'company')
    search_fields = ('sku', 'name', 'brand', 'model')

class AssetInline(admin.TabularInline):
    model = Asset
    extra = 1

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('catalogItem', 'serial', 'status', 'condition', 'location', 'company')
    list_filter = ('status', 'condition', 'location', 'company')
    search_fields = ('serial', 'catalogItem__name', 'catalogItem__sku')

@admin.register(Kit)
class KitAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'rate', 'company')
    list_filter = ('company',)
    search_fields = ('name', 'sku')

@admin.register(KitItem)
class KitItemAdmin(admin.ModelAdmin):
    list_display = ('kit', 'content_type', 'object_id', 'quantity')
    list_filter = ('kit', 'content_type')
    search_fields = ('kit__name', 'object_id')

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('code', 'caseType', 'weight', 'upright_only', 'company')
    list_filter = ('caseType', 'upright_only', 'company')
    search_fields = ('code',)

@admin.register(StockLocation)
class StockLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'address', 'company')
    list_filter = ('type', 'company')
    search_fields = ('name', 'address')
    inlines = [AssetInline]

@admin.register(Barcode)
class BarcodeAdmin(admin.ModelAdmin):
    list_display = ('value', 'entityType', 'entityId', 'company')
    list_filter = ('entityType', 'company')
    search_fields = ('value',)
