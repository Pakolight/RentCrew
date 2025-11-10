from django.contrib import admin
from .models import Clients, Contact

@admin.register(Clients)
class ClientsAdmin(admin.ModelAdmin):
    list_display = ('clientName', 'vatNumber')
    search_fields = ('clientName', 'vatNumber')
    list_filter = ('tags',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'role', 'email', 'phone')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('role',)
