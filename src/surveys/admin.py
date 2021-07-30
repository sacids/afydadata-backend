from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Survey, SurveyQuestions, SurveyResponses

admin.site.register(Survey)
admin.site.register(SurveyQuestions)
admin.site.register(SurveyResponses)