from django.contrib import admin
from .models import Venue, Vendor, TaxRule, PricePolicy

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'capacity')
    search_fields = ('name', 'address')

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'terms')
    search_fields = ('name',)

@admin.register(TaxRule)
class TaxRuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'rate', 'region')
    search_fields = ('name', 'region')

@admin.register(PricePolicy)
class PricePolicyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
