from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Company, User

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('legalName', 'tradeName', 'vatNumber', 'currency', 'country', 'city')
    list_filter = ('country', 'city')
    search_fields = ('legalName', 'tradeName', 'vatNumber', 'country', 'city')
    fieldsets = (
        ('Company Information', {'fields': ('legalName', 'tradeName', 'vatNumber', 'iban', 'currency', 'logo')}),
        ('Address', {'fields': ('country', 'street_address', 'city', 'state_province', 'zip_postal_code')}),
    )

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'company', 'is_staff')
    list_filter = ('role', 'company', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'role', 'company', 'avatar')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'role', 'company', 'avatar', 'is_staff', 'is_superuser'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
