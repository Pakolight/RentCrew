from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('projectId', 'itemType', 'refId', 'qty', 'dateFrom', 'dateTo', 'status')
    list_filter = ('itemType', 'status', 'dateFrom', 'dateTo')
    search_fields = ('projectId__name', 'lineId', 'refId')
