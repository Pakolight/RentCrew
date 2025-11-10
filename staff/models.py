from django.db import models

# Create your models here.
class Crew(models.Model):
    name = models.CharField(max_length=255)
    skills = models.JSONField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    rates = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "crews"

class Shift(models.Model):
    projectId = models.ForeignKey('projects.Project', related_name='shifts', on_delete=models.CASCADE)
    crewId = models.ForeignKey(Crew, related_name='shifts', on_delete=models.CASCADE)
    role = models.CharField(max_length=100)
    start = models.DateTimeField()
    end = models.DateTimeField()
    status = models.CharField(max_length=50)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.crewId.name} - {self.role} - {self.start.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name_plural = "shifts"

class Timesheet(models.Model):
    crewId = models.ForeignKey(Crew, related_name='timesheets', on_delete=models.CASCADE)
    projectId = models.ForeignKey('projects.Project', related_name='timesheets', on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    breaks = models.JSONField(blank=True, null=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.crewId.name} - {self.start.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name_plural = "timesheets"
