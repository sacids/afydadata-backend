from django.urls import path
from django.conf.urls import url

from . import views

app_name = "Survey"

urlpatterns = [
    path("form", views.xform_json, name="xfjs"),
    path("new/", views.SurveyCreateView.as_view(), name="new_survey"),
    path("list/", views.SurveyListView.as_view(), name="list_surveys"),
    path('<pk>/', views.SurveyDetailView.as_view(), name="show_survey"),

]