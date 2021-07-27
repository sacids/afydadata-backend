from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Survey(model.Model):
    title       = models.CharField(max_length=50)
    form_id     = models.CharField(max_length=50)
    filename    = models.FileField(upload_to='xform/defn/', max_length=100)

    class Meta:
        db_table = 'ad_surveys'
        managed = True

class SurveyQuestions(model.Model):

    QN_OPTIONS = (
        ('DATE', 'Date'),
        ('BARCODE', 'Barcode'),
        ('INT', 'Numeric'),
        ('GPS', 'gps'),
        ('TEXT', 'Text'),
        ('SELECT1', 'Select1'),
        ('SELECT', 'Select'),
        ('MEDIA', 'Media'),
        ('TIME', 'Time'),
    )

    survey      = models.ForeignKey('Survey', related_name='survey', on_delete=models.CASCADE)
    ref         = models.CharField(max_length=100,blank=True, null=True)
    title       = models.CharField(max_length=50)
    qn_type     = models.CharField(choices=QN_OPTIONS,default='TEXT')
    qn_options  = models.TextField(null=True,Blank=True)
    page        = models.CharField(max_length=2)
    created_on  = models.DateTimeField(auto_now=True)
    created_by  = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'ad_surveyQuestions'
        managed = True


class SurveyResponses(model.Model):
    survey          = models.ForeignKey('Survey', related_name='survey', on_delete=models.CASCADE)
    survey_question = models.ForeignKey('SurveyQuestions', related_name='survey_question', on_delete=models.CASCADE)
    response        = models.CharField(max_length=200)

    class Meta:
        db_table = 'ad_surveyResponses'
        managed = True