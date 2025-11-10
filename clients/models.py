from django.db import models
from company.models import Company

class Clients(models.Model):

    clientName = models.CharField(max_length=255)
    vatNumber = models.CharField(max_length=50, blank=True, null=True)
    billingAddress = models.TextField(blank=True, null=True)
    contacts = models.JSONField(blank=True, null=True)
    tags = models.JSONField(blank=True, null=True)
    company = models.ForeignKey(Company, related_name='clients', on_delete=models.CASCADE)

    def __str__(self):
        return self.clientName

    class Meta:
        verbose_name_plural = "accounts"


class Contact(models.Model):
    client = models.ForeignKey(Clients, related_name='clients_contacts', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "contacts"
