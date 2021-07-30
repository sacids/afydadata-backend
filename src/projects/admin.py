from django.contrib import admin

# Register your models here.
from .models import Project, ProjectMembers

admin.site.register(Project)
admin.site.register(ProjectMembers)