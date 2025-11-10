from django.contrib import admin
from .models import Account, Contact

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'vatNumber')
    search_fields = ('name', 'vatNumber')
    list_filter = ('type',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'account', 'role', 'email', 'phone')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('role',)
