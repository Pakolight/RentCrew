from django.contrib import admin
from .models import Quote, QuoteLine, QuoteSection, Invoice, Payment, SubRent

class QuoteLineInline(admin.TabularInline):
    model = QuoteLine
    extra = 1

class QuoteSectionInline(admin.TabularInline):
    model = QuoteSection
    extra = 1

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('number', 'version', 'status', 'projectId', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('number', 'projectId__name')
    inlines = [QuoteSectionInline, QuoteLineInline]

@admin.register(QuoteLine)
class QuoteLineAdmin(admin.ModelAdmin):
    list_display = ('quoteId', 'order', 'itemRef', 'qty', 'rate', 'days')
    list_filter = ('quoteId',)
    search_fields = ('itemRef',)

@admin.register(QuoteSection)
class QuoteSectionAdmin(admin.ModelAdmin):
    list_display = ('quoteId', 'order', 'name')
    list_filter = ('quoteId',)
    search_fields = ('name',)

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 1

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('number', 'status', 'projectId', 'dueDate', 'created_at')
    list_filter = ('status', 'dueDate', 'created_at')
    search_fields = ('number', 'projectId__name')
    inlines = [PaymentInline]

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('invoiceId', 'amount', 'date', 'method', 'ref')
    list_filter = ('method', 'date')
    search_fields = ('ref', 'invoiceId__number')

@admin.register(SubRent)
class SubRentAdmin(admin.ModelAdmin):
    list_display = ('projectId', 'dateFrom', 'dateTo', 'cost')
    list_filter = ('dateFrom', 'dateTo')
    search_fields = ('projectId__name',)
