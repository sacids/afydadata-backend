from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Project(models.Model):
    title           = models.CharField(max_length=50)
    description     = models.TextField()
    created_on      = models.DateTimeField(auto_now=True)
    created_by      = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    class Meta:
        db_table    = 'ad_projects'
        managed     = True


class ProjectMembers(models.Model):
    project         = models.ForeignKey(Project, on_delete=models.CASCADE)
    member          = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    class Meta:
        db_table    = 'ad_projectMembers'
        managed     = True