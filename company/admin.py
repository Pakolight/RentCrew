from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Company, User

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('legalName', 'tradeName', 'vatNumber', 'currency')
    search_fields = ('legalName', 'tradeName', 'vatNumber')

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'company', 'is_staff')
    list_filter = ('role', 'company', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'company')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('role', 'company')}),
    )
