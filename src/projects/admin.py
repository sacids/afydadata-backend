from django.contrib import admin

# Register your models here.
from .models import Project, ProjectMember, ProjectGroup

#admin.site.register(Project)
admin.site.register(ProjectMember)
#admin.site.register(ProjectGroup)



class ProjectGroupInline(admin.StackedInline):
    model = ProjectGroup
class ProjectAdmin(admin.ModelAdmin):
    inlines =[ProjectGroupInline]
    
admin.site.register(Project,ProjectAdmin)

