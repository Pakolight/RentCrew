from django.contrib import admin
from .models import Crew, Shift, Timesheet

@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'email', 'phone')

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('crewId', 'projectId', 'role', 'start', 'end', 'status', 'confirmed')
    list_filter = ('status', 'confirmed', 'role', 'start')
    search_fields = ('crewId__name', 'projectId__name', 'role')

@admin.register(Timesheet)
class TimesheetAdmin(admin.ModelAdmin):
    list_display = ('crewId', 'projectId', 'start', 'end', 'approved')
    list_filter = ('approved', 'start')
    search_fields = ('crewId__name', 'projectId__name')
