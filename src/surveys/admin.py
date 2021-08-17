from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Survey, SurveyQuestions, SurveyResponses, SurveyFilter, SurveyPerm

admin.site.register(Survey)
admin.site.register(SurveyResponses)
admin.site.register(SurveyFilter)
admin.site.register(SurveyPerm)




class SurveyQuestionsAdmin(admin.ModelAdmin):
    list_display = ['survey','ref' ,'col_name' ,'col_type' ,'page' ,'order' ]
    list_filter = ['survey']

admin.site.register(SurveyQuestions,SurveyQuestionsAdmin)