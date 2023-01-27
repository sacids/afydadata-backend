from django.urls import path
from django.conf.urls import url

from . import views
from . import ajax_datatable_views

app_name = "ui"

urlpatterns = [
    path("", views.start.as_view(), name="start"),

    path('ajax_datatable/permissions/', ajax_datatable_views.PermissionAjaxDatatableView.as_view(), name="ajax_datatable_permissions"),
    path('ajax_datatable/survey_list/', ajax_datatable_views.SurveyList.as_view(), name="surveylist"),
    
]