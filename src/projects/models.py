import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Project(models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title           = models.CharField(max_length=50)
    description     = models.TextField()
    created_on      = models.DateTimeField(auto_now=True,null=True)
    created_by      = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    
    class Meta:
        db_table    = 'ad_projects'
        managed     = True
        app_label   = 'projects'
    
    def __str__(self):
        return self.title if self.title else self.pk
    
    def get_absolute_url(self):
        return reverse('project_detail', args={'pk': self.id})



class ProjectGroup(models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project         = models.ForeignKey(Project, related_name='project_groups', on_delete=models.CASCADE)
    title           = models.CharField(max_length=100)
    class Meta:
        db_table    = 'ad_projectGroups'
        managed     = True
        app_label   = 'projects'
    
    def __str__(self):
        return self.project.title+' : '+self.title if self.title else self.pk

class ProjectMember(models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project         = models.ForeignKey(Project, related_name='project_member', on_delete=models.CASCADE,default=1)
    projectGroup    = models.ManyToManyField(ProjectGroup, related_name='pm_groups')
    member          = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    
    class Meta:
        db_table    = 'ad_projectMembers'
        managed     = True
        app_label   = 'projects'

    def __str__(self):
        return self.member.username


# create
@receiver(post_save, sender=Project)
def initiate_project(sender, instance, created, **kwargs):
    if created:
        # create project viewer group
        PG_Viewer       = ProjectGroup.objects.create(project=instance,title="DataViewers")
        PG_Collector    = ProjectGroup.objects.create(project=instance,title="DataCollectors")

        # Add membership to current user
        PG_Member       = ProjectMember.objects.create(projectGroup=PG_Viewer,member=instance.created_by)
        PG_Member       = ProjectMember.objects.create(projectGroup=PG_Collector,member=instance.created_by)

