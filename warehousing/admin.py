from django.contrib import admin
from .models import Shipment, Picklist, Scan

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('projectId', 'type', 'plannedAt', 'actualAt', 'carrier', 'vehicle', 'driver')
    list_filter = ('type', 'plannedAt', 'actualAt')
    search_fields = ('projectId__name', 'carrier', 'driver', 'notes')

@admin.register(Picklist)
class PicklistAdmin(admin.ModelAdmin):
    list_display = ('projectId', 'version', 'status')
    list_filter = ('status', 'version')
    search_fields = ('projectId__name',)

@admin.register(Scan)
class ScanAdmin(admin.ModelAdmin):
    list_display = ('barcode', 'entityType', 'action', 'timestamp', 'userId', 'projectId')
    list_filter = ('entityType', 'action', 'timestamp')
    search_fields = ('barcode', 'userId__username', 'projectId__name')
