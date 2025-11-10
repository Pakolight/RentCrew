from django.db import models
from django.contrib.auth.models import AbstractUser

class Company(models.Model):
    legalName = models.CharField(max_length=255)
    tradeName = models.CharField(max_length=255, blank=True, null=True)
    vatNumber = models.CharField(max_length=50, blank=True, null=True)
    iban = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    contacts = models.JSONField(blank=True, null=True)
    branding = models.JSONField(blank=True, null=True)
    currency = models.CharField(max_length=3, blank=True, null=True)

    def __str__(self):
        return self.legalName

    class Meta:
        verbose_name_plural = "companies"

class User(AbstractUser):
    role = models.CharField(max_length=50)
    # В модели User
    company = models.ForeignKey('company.Company', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name_plural = "users"

    # Add related_name to avoid clashes with auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='company_user_set',
        related_query_name='company_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='company_user_set',
        related_query_name='company_user',
    )
