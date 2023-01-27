from django.shortcuts import render
from django.views import generic

# Create your views here.



class start(generic.TemplateView):
    template_name = "pages/start.html"