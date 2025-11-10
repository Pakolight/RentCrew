from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import UniqueConstraint, Max, F, CheckConstraint, Q


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

    # Reference to Project model from projects app
    projectId = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='quotes')
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
    Model for individual line items in quotes with ordered positioning.

    The `order` field implements a position-based ordering system:
    - When order=None on creation: automatically appended at the end (max(order)+1)
    - When order is specified on creation: inserted at that position, shifting existing items
    - When updating order: appropriate shifting occurs to maintain consistent ordering
    """
    # Maximum allowed order value to prevent integer overflow issues
    MAX_ORDER = 1000000

    quoteId = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='lines')
    order = models.PositiveIntegerField(null=True, blank=True)  # Intentionally no default
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
        ordering = ["order", "id"]
        constraints = [
            UniqueConstraint(fields=["quoteId", "order"], name="uniq_quoteline_order"),
            # Ensure order is always positive when specified
            CheckConstraint(
                check=Q(order__isnull=True) | Q(order__gt=0),
                name="check_quoteline_order_positive"
            ),
        ]
        # Add index for better performance on common queries
        indexes = [
            models.Index(fields=["quoteId", "order"], name="idx_quoteline_quote_order"),
        ]
        verbose_name_plural = "quote lines"

    def clean(self):
        """Validate model data before saving"""
        super().clean()
        if self.order is not None:
            if self.order <= 0:
                raise ValidationError({"order": "Order must be a positive integer"})
            if self.order > self.MAX_ORDER:
                raise ValidationError({"order": f"Order cannot exceed {self.MAX_ORDER}"})

    def save(self, *args, **kwargs):
        """
        Save the model with proper ordering logic.

        Handles:
        - Creation with order=None (append at end)
        - Creation with specific order (insert with shifting)
        - Updates that change order (with appropriate shifting)
        """
        self.clean()
        is_create = self.pk is None

        with transaction.atomic():
            if is_create:
                # Creation
                if self.order is None:
                    # Append at end: max(order) + 1
                    last = (
                            QuoteLine.objects
                            .select_for_update()
                            .filter(quoteId=self.quoteId)
                            .aggregate(max_o=Max("order"))["max_o"] or 0
                    )
                    self.order = last + 1
                else:
                    # Insert at specific position: shift all >= self.order
                    (QuoteLine.objects
                     .select_for_update()
                     .filter(quoteId=self.quoteId, order__gte=self.order)
                     .update(order=F("order") + 1))
            else:
                # Update existing record
                # Get old record with select_for_update to prevent race conditions
                old = QuoteLine.objects.select_for_update().get(pk=self.pk)

                if self.order is None:
                    # If order not specified, keep previous order
                    self.order = old.order
                elif self.order != old.order:
                    # Only process if order actually changed
                    if self.order < old.order:
                        # Moving up: shift [new, old-1] down by +1
                        (QuoteLine.objects
                         .select_for_update()
                         .filter(
                            quoteId=self.quoteId,
                            order__gte=self.order,
                            order__lt=old.order,
                        )
                         .update(order=F("order") + 1))
                    else:
                        # Moving down: shift [old+1, new] up by -1
                        (QuoteLine.objects
                         .select_for_update()
                         .filter(
                            quoteId=self.quoteId,
                            order__gt=old.order,
                            order__lte=self.order,
                        )
                         .update(order=F("order") - 1))

            super().save(*args, **kwargs)

    # Helper methods for common operations
    @classmethod
    def insert_at(cls, quote, position, **fields):
        """
        Insert a new line at a specific position.

        Args:
            quote: The Quote object or ID
            position: The order position to insert at
            **fields: Additional fields for the new line

        Returns:
            The newly created QuoteLine
        """
        line = cls(quoteId=quote, order=position, **fields)
        line.save()
        return line

    def move_to(self, position):
        """
        Move this line to a new position.

        Args:
            position: The new order position

        Returns:
            self (for method chaining)
        """
        self.order = position
        self.save()
        return self

    @classmethod
    def reindex(cls, quote):
        """
        Reindex all lines to remove gaps.

        Args:
            quote: The Quote object or ID
        """
        with transaction.atomic():
            lines = list(cls.objects.select_for_update()
                        .filter(quoteId=quote)
                        .order_by('order', 'id'))
            for i, line in enumerate(lines, 1):
                if line.order != i:
                    line.order = i
                    line.save(update_fields=['order'])


class QuoteSection(models.Model):
    """
    Quote sections with ordered positioning.

    The `order` field implements a position-based ordering system:
    - When order=None on creation: automatically appended at the end (max(order)+1)
    - When order is specified on creation: inserted at that position, shifting existing items
    - When updating order: appropriate shifting occurs to maintain consistent ordering
    """
    # Maximum allowed order value to prevent integer overflow issues
    MAX_ORDER = 1000000

    quoteId = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='sections')
    order = models.PositiveIntegerField(null=True, blank=True)  # Intentionally no default
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["order", "id"]
        constraints = [
            UniqueConstraint(fields=["quoteId", "order"], name="uniq_quote_section_order"),
            # Ensure order is always positive when specified
            CheckConstraint(
                check=Q(order__isnull=True) | Q(order__gt=0),
                name="check_order_positive"
            ),
        ]
        # Add index for better performance on common queries
        indexes = [
            models.Index(fields=["quoteId", "order"], name="idx_quotesection_quote_order"),
        ]
        verbose_name_plural = "quote sections"

    def clean(self):
        """Validate model data before saving"""
        super().clean()
        if self.order is not None:
            if self.order <= 0:
                raise ValidationError({"order": "Order must be a positive integer"})
            if self.order > self.MAX_ORDER:
                raise ValidationError({"order": f"Order cannot exceed {self.MAX_ORDER}"})

    def save(self, *args, **kwargs):
        """
        Save the model with proper ordering logic.

        Handles:
        - Creation with order=None (append at end)
        - Creation with specific order (insert with shifting)
        - Updates that change order (with appropriate shifting)
        """
        self.clean()
        is_create = self.pk is None

        with transaction.atomic():
            if is_create:
                # Creation
                if self.order is None:
                    # Append at end: max(order) + 1
                    last = (
                            QuoteSection.objects
                            .select_for_update()
                            .filter(quoteId=self.quoteId)
                            .aggregate(max_o=Max("order"))["max_o"] or 0
                    )
                    self.order = last + 1
                else:
                    # Insert at specific position: shift all >= self.order
                    (QuoteSection.objects
                     .select_for_update()
                     .filter(quoteId=self.quoteId, order__gte=self.order)
                     .update(order=F("order") + 1))
            else:
                # Update existing record
                # Get old record with select_for_update to prevent race conditions
                old = QuoteSection.objects.select_for_update().get(pk=self.pk)

                if self.order is None:
                    # If order not specified, keep previous order
                    self.order = old.order
                elif self.order != old.order:
                    # Only process if order actually changed
                    if self.order < old.order:
                        # Moving up: shift [new, old-1] down by +1
                        (QuoteSection.objects
                         .select_for_update()
                         .filter(
                            quoteId=self.quoteId,
                            order__gte=self.order,
                            order__lt=old.order,
                        )
                         .update(order=F("order") + 1))
                    else:
                        # Moving down: shift [old+1, new] up by -1
                        (QuoteSection.objects
                         .select_for_update()
                         .filter(
                            quoteId=self.quoteId,
                            order__gt=old.order,
                            order__lte=self.order,
                        )
                         .update(order=F("order") - 1))

            super().save(*args, **kwargs)

    # Helper methods for common operations
    @classmethod
    def insert_at(cls, quote, position, **fields):
        """
        Insert a new section at a specific position.

        Args:
            quote: The Quote object or ID
            position: The order position to insert at
            **fields: Additional fields for the new section

        Returns:
            The newly created QuoteSection
        """
        section = cls(quoteId=quote, order=position, **fields)
        section.save()
        return section

    def move_to(self, position):
        """
        Move this section to a new position.

        Args:
            position: The new order position

        Returns:
            self (for method chaining)
        """
        self.order = position
        self.save()
        return self

    @classmethod
    def reindex(cls, quote):
        """
        Reindex all sections to remove gaps.

        Args:
            quote: The Quote object or ID
        """
        with transaction.atomic():
            sections = list(cls.objects.select_for_update()
                            .filter(quoteId=quote)
                            .order_by('order', 'id'))
            for i, section in enumerate(sections, 1):
                if section.order != i:
                    section.order = i
                    section.save(update_fields=['order'])



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

    # Reference to Project model from projects app
    projectId = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='invoices')
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
    # Reference to Project model from projects app
    projectId = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='subrents')
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
