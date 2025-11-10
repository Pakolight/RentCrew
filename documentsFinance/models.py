from django.db import models
from django.utils import timezone

class Quote(models.Model):
    """
    Model for project quotes.
    Tracks quotes with version control and status tracking.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    # Using string reference for Project model as it might not exist yet
    projectId = models.ForeignKey('company.Project', on_delete=models.CASCADE, related_name='quotes')
    number = models.CharField(max_length=50)
    version = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    totals = models.JSONField(help_text="JSON containing subtotal, tax, discount, and total amounts")
    pdf = models.FileField(upload_to='quotes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Quote {self.number} v{self.version} - {self.get_status_display()}"

    class Meta:
        verbose_name_plural = "quotes"


class QuoteLine(models.Model):
    """
    Model for individual line items in quotes.
    """
    quoteId = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='lines')
    itemRef = models.CharField(max_length=100, help_text="Reference to catalog item, kit, or other item")
    qty = models.PositiveIntegerField(default=1)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    days = models.PositiveIntegerField(default=1)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Discount percentage")
    taxRuleId = models.ForeignKey('refdata.TaxRule', on_delete=models.SET_NULL, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Line {self.id} - {self.itemRef} x{self.qty}"

    class Meta:
        verbose_name_plural = "quote lines"


class Invoice(models.Model):
    """
    Model for project invoices.
    Tracks invoices with status tracking and due dates.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    ]

    # Using string reference for Project model as it might not exist yet
    projectId = models.ForeignKey('company.Project', on_delete=models.CASCADE, related_name='invoices')
    number = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    dueDate = models.DateField()
    totals = models.JSONField(help_text="JSON containing subtotal, tax, discount, and total amounts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Invoice {self.number} - {self.get_status_display()}"

    class Meta:
        verbose_name_plural = "invoices"


class Payment(models.Model):
    """
    Model for tracking payments against invoices.
    """
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('credit_card', 'Credit Card'),
        ('check', 'Check'),
        ('other', 'Other'),
    ]

    invoiceId = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    ref = models.CharField(max_length=100, blank=True, null=True, help_text="Reference number or transaction ID")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.id} - {self.amount} ({self.get_method_display()})"

    class Meta:
        verbose_name_plural = "payments"


class SubRent(models.Model):
    """
    Model for tracking items rented from external vendors.
    """
    # Using string reference for Project model as it might not exist yet
    projectId = models.ForeignKey('company.Project', on_delete=models.CASCADE, related_name='subrents')
    items = models.JSONField(help_text="JSON array of items being rented")
    dateFrom = models.DateTimeField()
    dateTo = models.DateTimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"SubRent {self.id} - {self.dateFrom.date()} to {self.dateTo.date()}"

    class Meta:
        verbose_name_plural = "sub rents"
