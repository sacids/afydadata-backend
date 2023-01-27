from django.urls import path
from django.conf.urls import url

from . import views

app_name = "ui"

urlpatterns = [
    path("", views.start, name="start"),

]