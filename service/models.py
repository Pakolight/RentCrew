from django.db import models
from projects.models import Project
from equipment.models import Asset

# Create your models here.
class Maintenance(models.Model):
    TYPE_CHOICES = (
        ('inspection', 'Inspection'),
        ('repair', 'Repair'),
        ('PAT', 'PAT'),
    )

    assetId = models.ForeignKey(Asset, related_name='maintenances', on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    dueAt = models.DateTimeField()
    completedAt = models.DateTimeField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_type_display()} for {self.assetId} due at {self.dueAt.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name_plural = "maintenances"

class Damage(models.Model):
    SEVERITY_CHOICES = (
        ('minor', 'Minor'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
    )

    COST_RECOVERY_CHOICES = (
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
        ('internal', 'Internal'),
    )

    projectId = models.ForeignKey(Project, related_name='damages', on_delete=models.CASCADE)
    assetId = models.ForeignKey(Asset, related_name='damages', on_delete=models.CASCADE)
    reportedAt = models.DateTimeField(auto_now_add=True)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    description = models.TextField()
    costRecovery = models.CharField(max_length=20, choices=COST_RECOVERY_CHOICES)

    def __str__(self):
        return f"{self.get_severity_display()} damage to {self.assetId} on {self.reportedAt.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name_plural = "damages"
