from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Disease)
admin.site.register(SymptomToDisease)
admin.site.register(Specie)



class SymptomAdmin(admin.ModelAdmin):
    list_display = ['code','title']

admin.site.register(Symptom,SymptomAdmin)