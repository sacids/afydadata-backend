from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from _datetime import timedelta
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
class Survey(models.Model):
    title       = models.CharField(max_length=50)
    form_id     = models.CharField(max_length=50)
    xform       = models.FileField(upload_to='xform/defn/', max_length=100)
    description = models.TextField()
    created_on  = models.DateTimeField(auto_now=True)
    created_by  = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'ad_surveys'
        managed = True

    def __str__(self):
        return self.title if self.title else self.pk

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
    qn_options  = models.TextField(null=True,blank=True)
    order       = models.IntegerField(blank=True, null=True,default=0)
    page        = models.CharField(max_length=2,blank=True, null=True)
    created_on  = models.DateTimeField(auto_now=True)
    created_by  = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'ad_surveyQuestions'
        managed = True


class SurveyResponses(models.Model):
    survey          = models.ForeignKey('Survey', related_name='survey_responses', on_delete=models.CASCADE)
    instance_id     = models.CharField(max_length=100,blank=False,null=False,unique=True)
    response        = models.JSONField()
    created_on      = models.DateTimeField(auto_now=True)
    created_by      = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'ad_surveyResponses'
        managed = True