from django.db import models
from clients.models import Clients
from refdata.models import Venue
from company.models import User
from staff.models import Crew

class Project(models.Model):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    stage = models.CharField(max_length=50)
    account = models.ForeignKey(Clients, related_name='projects', on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, related_name='projects', on_delete=models.CASCADE)
    eventDates = models.JSONField(help_text='Contains loadIn, showStart, showEnd, loadOut dates')
    ownerUser = models.ForeignKey(User, related_name='owned_projects', on_delete=models.CASCADE)
    probability = models.IntegerField(help_text='Probability percentage of project happening')
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name_plural = "projects"

class ProjectNotes(models.Model):
    project = models.ForeignKey(Project, related_name='project_notes', on_delete=models.CASCADE)
    text = models.TextField()
    pinned = models.BooleanField(default=False)
    attachments = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Note for {self.project.name} - {self.created_at.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name_plural = "project notes"

class ProjectFiles(models.Model):
    project = models.ForeignKey(Project, related_name='project_files', on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)
    file_size = models.IntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, related_name='uploaded_files', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.file_name

    class Meta:
        verbose_name_plural = "project files"

class ProjectTasks(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    project = models.ForeignKey(Project, related_name='project_tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due = models.DateTimeField(blank=True, null=True)
    assignee = models.ForeignKey(User, related_name='assigned_tasks', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "project tasks"

class ProjectCrewNeeds(models.Model):
    project = models.ForeignKey(Project, related_name='crew_needs', on_delete=models.CASCADE)
    role = models.CharField(max_length=100)
    qty = models.IntegerField()
    day_time = models.JSONField(help_text='Day and time information for the crew need')
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    assigned_crew = models.ManyToManyField(Crew, related_name='assigned_needs', blank=True)

    def __str__(self):
        return f"{self.role} ({self.qty}) for {self.project.name}"

    class Meta:
        verbose_name_plural = "project crew needs"

class ProjectLogistics(models.Model):
    DELIVERY_TYPE_CHOICES = (
        ('pickup', 'Pickup'),
        ('delivery', 'Delivery'),
        ('shipping', 'Shipping'),
    )

    project = models.ForeignKey(Project, related_name='logistics', on_delete=models.CASCADE)
    delivery_type = models.CharField(max_length=20, choices=DELIVERY_TYPE_CHOICES, default='delivery')
    address = models.TextField()
    windows = models.JSONField(help_text='Time windows for delivery/pickup')
    vehicle_needs = models.TextField(blank=True, null=True)
    parking_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Logistics for {self.project.name}"

    class Meta:
        verbose_name_plural = "project logistics"
