from django.db import models
from company.models import Company

class Venue(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    contact = models.JSONField(blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    company = models.ForeignKey(Company, related_name='venues', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "venues"


class Vendor(models.Model):
    name = models.CharField(max_length=255)
    terms = models.TextField(blank=True, null=True)
    contacts = models.JSONField(blank=True, null=True)
    company = models.ForeignKey(Company, related_name='venues', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "vendors"


class TaxRule(models.Model):
    name = models.CharField(max_length=255)
    rate = models.DecimalField(max_digits=5, decimal_places=2)
    region = models.CharField(max_length=255, blank=True, null=True)
    company = models.ForeignKey(Company, related_name='venues', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "tax rules"


class PricePolicy(models.Model):
    name = models.CharField(max_length=255)
    degressive = models.JSONField(blank=True, null=True)
    weekendRule = models.JSONField(blank=True, null=True)
    overtimeRule = models.JSONField(blank=True, null=True)
    company = models.ForeignKey(Company, related_name='venues', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "price policies"
