from django.db import models
from projects.models import Project
from company.models import User

# Create your models here.
class Shipment(models.Model):
    TYPE_CHOICES = (
        ('delivery', 'Delivery'),
        ('pickup', 'Pickup'),
        ('return', 'Return'),
    )

    projectId = models.ForeignKey(Project, related_name='shipments', on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    plannedAt = models.DateTimeField()
    actualAt = models.DateTimeField(blank=True, null=True)
    carrier = models.CharField(max_length=255, blank=True, null=True)
    vehicle = models.CharField(max_length=255, blank=True, null=True)
    driver = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_type_display()} for {self.projectId.name} on {self.plannedAt.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name_plural = "shipments"

class Picklist(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    projectId = models.ForeignKey(Project, related_name='picklists', on_delete=models.CASCADE)
    version = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    lines = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"Picklist v{self.version} for {self.projectId.name}"

    class Meta:
        verbose_name_plural = "picklists"

class Scan(models.Model):
    ENTITY_TYPE_CHOICES = (
        ('asset', 'Asset'),
        ('case', 'Case'),
    )

    ACTION_CHOICES = (
        ('checkOut', 'Check Out'),
        ('checkIn', 'Check In'),
    )

    entityType = models.CharField(max_length=20, choices=ENTITY_TYPE_CHOICES)
    barcode = models.CharField(max_length=255)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    userId = models.ForeignKey(User, related_name='scans', on_delete=models.CASCADE)
    projectId = models.ForeignKey(Project, related_name='scans', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_action_display()} {self.get_entity_type_display()} {self.barcode}"

    class Meta:
        verbose_name_plural = "scans"
