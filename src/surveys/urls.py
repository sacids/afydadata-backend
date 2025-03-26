from django.urls import path

from . import views

app_name = "Survey"

urlpatterns = [
    path("form", views.init_xform, name="xfjs"),
    path("new/", views.SurveyCreateView.as_view(), name="new_survey"),
    path("list/", views.SurveyListView.as_view(), name="list_surveys"),
    path('<pk>/', views.SurveyDetailView.as_view(), name="show_survey"),

]