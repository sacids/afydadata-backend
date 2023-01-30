from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from _datetime import timedelta
from django.urls import reverse
from django.utils.text import slugify
from projects.models import Project, ProjectGroup
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Survey(models.Model):
    project     = models.ForeignKey('projects.Project', related_name='project',default=1, on_delete=models.CASCADE)
    title       = models.CharField(max_length=50)
    form_id     = models.CharField(max_length=250)
    xform       = models.FileField(upload_to='xform/defn/', max_length=100)
    description = models.TextField()
    created_on  = models.DateTimeField(auto_now=True)
    created_by  = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'ad_surveys'
        managed = True
        app_label = 'surveys'

    def __str__(self):
        return self.title if self.title else self.pk
    
    def get_absolute_url(self):
        return reverse('form_data', args={'pk': self.id, 'project_id':self.project.id})

class SurveyQuestions(models.Model):

    QN_OPTIONS = (
        ('DATE', 'Date'),
        ('BARCODE', 'Barcode'),
        ('INT', 'Numeric'),
        ('GEOPOINT', 'Geopoint'),
        ('TEXT', 'String'),
        ('INT', 'int'),
        ('SELECT1', 'Select1'),
        ('SELECT', 'Select'),
        ('BINARY', 'Binary'),
        ('TIME', 'Time'),
        ('DATETIME', 'DateTime'),
    )

    survey      = models.ForeignKey('Survey', related_name='survey_questions', on_delete=models.CASCADE)
    ref         = models.CharField(max_length=100,blank=True, null=True)
    col_name    = models.CharField(max_length=50)
    col_type    = models.CharField(max_length=10,choices=QN_OPTIONS,default='TEXT')
    options     = models.TextField(null=True,blank=True)
    hint        = models.TextField(null=True,blank=True)
    label       = models.TextField(null=True,blank=True)
    constraints = models.TextField(blank=True, null=True)
    required    = models.CharField(max_length=1,default=0)
    order       = models.IntegerField(blank=True, null=True,default=0)
    page        = models.CharField(max_length=2,blank=True, null=True)

    class Meta:
        db_table = 'ad_surveyQuestions'
        managed = True
        app_label = 'surveys'


class SurveyResponses(models.Model):
    survey          = models.ForeignKey('Survey', related_name='survey_responses', on_delete=models.CASCADE)
    instance_id     = models.CharField(max_length=100,blank=False,null=False)
    response        = models.JSONField(null=False)
    created_on      = models.DateTimeField(auto_now=True)
    created_by      = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'ad_surveyResponses'
        managed = True
        app_label = 'surveys'

    
    def __str__(self):
        return self.instance_id if self.instance_id else self.pk


class SurveyFilter(models.Model):
    survey          = models.ForeignKey('Survey', related_name='survey_filters', on_delete=models.CASCADE)
    title           = models.CharField(max_length=100,blank=False,null=False)
    data_filter     = models.TextField()
    class Meta:
        db_table = 'ad_surveyFilters'
        managed = True
        app_label = 'surveys'
    
    def __str__(self):
        return self.title if self.title else self.pk


class SurveyPerm(models.Model):
    survey          = models.ForeignKey('Survey', related_name='survey_perms', on_delete=models.CASCADE)
    project_group   = models.ForeignKey('projects.ProjectGroup', related_name='project_group', on_delete=models.CASCADE)
    data_filter     = models.ForeignKey('SurveyFilter', related_name='filter', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'ad_surveyPerms'
        managed = True
        app_label = 'surveys'