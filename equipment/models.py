from django.db import models
from company.models import Company
from refdata.models import PricePolicy
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType




# CatalogItem model for equipment catalog
class CatalogItem(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    sellable = models.BooleanField(default=False)
    rentable = models.BooleanField(default=True)
    isConsumable = models.BooleanField(default=False)
    defaultRate = models.DecimalField(max_digits=10, decimal_places=2)
    pricePolicy = models.ForeignKey(PricePolicy, on_delete=models.SET_NULL, blank=True, null=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    power = models.CharField(max_length=100, blank=True, null=True)
    dimensions = models.JSONField(blank=True, null=True)  # Store as {length, width, height, unit}
    upright_only = models.BooleanField(default=False)
    image = models.ImageField(upload_to='catalog_items/', blank=True, null=True)
    company = models.ForeignKey(Company, related_name='catalog_items', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.sku} - {self.name}"

    class Meta:
        verbose_name_plural = "catalog items"

# Asset model for individual equipment items
class Asset(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('maintenance', 'Under Maintenance'),
        ('damaged', 'Damaged'),
        ('retired', 'Retired'),
    ]

    CONDITION_CHOICES = [
        ('new', 'New'),
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ]

    catalogItem = models.ForeignKey(CatalogItem, related_name='assets', on_delete=models.CASCADE)
    serial = models.CharField(max_length=100, blank=True, null=True)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='good')
    location = models.ForeignKey('StockLocation', related_name='stored_assets', on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    company = models.ForeignKey(Company, related_name='assets', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.catalogItem.name} - {self.serial}"

    class Meta:
        verbose_name_plural = "assets"

# Kit model for equipment bundles
class Kit(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=50, unique=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    items = models.JSONField()  # Store as [{catalogItemId|kitId, qty}]
    company = models.ForeignKey(Company, related_name='kits', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "kits"


class KitItem(models.Model):
    kit = models.ForeignKey('Kit', on_delete=models.CASCADE, related_name='kit_items')

    # Generic Foreign Key for communication with different models
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')

    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('kit', 'content_type', 'object_id')


# Case model for storage containers
class Case(models.Model):
    CASE_TYPE_CHOICES = [
        ('flight', 'Flight Case'),
        ('pelican', 'Pelican Case'),
        ('road', 'Road Case'),
        ('soft', 'Soft Case'),
        ('other', 'Other'),
    ]

    code = models.CharField(max_length=50, unique=True)
    caseType = models.CharField(max_length=20, choices=CASE_TYPE_CHOICES)
    weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    contents = models.JSONField(blank=True, null=True)  # Store references to assets or other items
    company = models.ForeignKey(Company, related_name='cases', on_delete=models.CASCADE)
    upright_only = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.code} ({self.get_caseType_display()})"

    class Meta:
        verbose_name_plural = "cases"

# StockLocation model for where equipment is stored
class StockLocation(models.Model):
    LOCATION_TYPE_CHOICES = [
        ('warehouse', 'Warehouse'),
        ('truck', 'Truck'),
        ('shelf', 'Shelf'),
    ]

    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=20, choices=LOCATION_TYPE_CHOICES)
    image = models.ImageField(upload_to='stock_locations/', blank=True, null=True)
    company = models.ForeignKey(Company, related_name='stock_locations', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

    class Meta:
        verbose_name_plural = "stock locations"

# Barcode model for tracking equipment
class Barcode(models.Model):
    ENTITY_TYPE_CHOICES = [
        ('asset', 'Asset'),
        ('case', 'Case'),
        ('catalog_item', 'Catalog Item'),
        ('kit', 'Kit'),
    ]

    value = models.CharField(max_length=100, unique=True)
    entityType = models.CharField(max_length=20, choices=ENTITY_TYPE_CHOICES)
    entityId = models.IntegerField()
    company = models.ForeignKey(Company, related_name='barcodes', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.value} ({self.get_entityType_display()})"

    class Meta:
        verbose_name_plural = "barcodes"
