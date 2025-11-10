from django.contrib import admin
from .models import Maintenance, Damage

@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('assetId', 'type', 'dueAt', 'completedAt', 'cost')
    list_filter = ('type', 'dueAt', 'completedAt')
    search_fields = ('assetId__serial', 'assetId__catalogItem__name', 'notes')

@admin.register(Damage)
class DamageAdmin(admin.ModelAdmin):
    list_display = ('assetId', 'projectId', 'severity', 'reportedAt', 'costRecovery')
    list_filter = ('severity', 'costRecovery', 'reportedAt')
    search_fields = ('assetId__serial', 'assetId__catalogItem__name', 'projectId__name', 'description')
