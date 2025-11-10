from django.contrib import admin
from .models import Project, ProjectNotes, ProjectFiles, ProjectTasks, ProjectCrewNeeds, ProjectLogistics

# Register your models here.
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'stage', 'account', 'venue', 'probability', 'budget')
    search_fields = ('code', 'name')
    list_filter = ('stage', 'probability')

@admin.register(ProjectNotes)
class ProjectNotesAdmin(admin.ModelAdmin):
    list_display = ('project', 'pinned', 'created_at')
    search_fields = ('project__name', 'text')
    list_filter = ('pinned', 'created_at')

@admin.register(ProjectFiles)
class ProjectFilesAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'project', 'file_type', 'uploaded_at', 'uploaded_by')
    search_fields = ('file_name', 'project__name')
    list_filter = ('file_type', 'uploaded_at')

@admin.register(ProjectTasks)
class ProjectTasksAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'due', 'assignee', 'status')
    search_fields = ('title', 'project__name')
    list_filter = ('status', 'due')

@admin.register(ProjectCrewNeeds)
class ProjectCrewNeedsAdmin(admin.ModelAdmin):
    list_display = ('role', 'qty', 'project', 'rate')
    search_fields = ('role', 'project__name')
    list_filter = ('role',)

@admin.register(ProjectLogistics)
class ProjectLogisticsAdmin(admin.ModelAdmin):
    list_display = ('project', 'delivery_type', 'address')
    search_fields = ('project__name', 'address')
    list_filter = ('delivery_type',)
