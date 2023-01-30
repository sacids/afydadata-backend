from django.urls import path
from django.conf.urls import url

from . import views
from . import ajax_datatable_views

#app_name = "ui"

urlpatterns = [
    path("", views.start.as_view(), name="start"),
    path("start", views.start.as_view(), name="start"),

    path('ajax_datatable/permissions/', ajax_datatable_views.PermissionAjaxDatatableView.as_view(), name="ajax_datatable_permissions"),
    path('ajax_datatable/survey_list/', ajax_datatable_views.SurveyList.as_view(), name="surveylist"),
    path('ajax_datatable/project_list/', ajax_datatable_views.ProjectList.as_view(), name="projectList"),
    path('ajax_datatable/form_data/', ajax_datatable_views.formData.as_view(), name="formData"),
    
    #start
    path('tutorial', views.list_projects.as_view(), name="tutorial"),
    path('case_studies', views.list_projects.as_view(), name="case_studies"),
    path('awknolegements', views.list_projects.as_view(), name="awknoledgement"),
    
    #Projects
    path('project/dashboard', views.list_projects.as_view(), name="project_dashboard"),
    path('project/list', views.list_projects.as_view(), name="list_projects"),
    path('project/<pk>', views.project_detail.as_view(), name="project_detail"),
    #path('project/delete/<pk>', views.list_projects.as_view(), name="project_delete"),
    path('project/members', views.list_projects.as_view(), name="list_members"),
    path('project/create', views.create_project.as_view(), name="create_project" ),
    
    
    path('project/<pk>/form/create', views.create_xform.as_view(), name="create_xform"),
    
    
    # Form
    path('project/<int:project_id>/form/<pk>/data', views.form_data.as_view(), name="form_data"),
    path('project/<int:project_id>/form/<pk>/map', views.create_xform.as_view(), name="form_map"),
    path('project/<int:project_id>/form/<pk>/chart', views.create_xform.as_view(), name="form_chart"),
    path('project/<int:project_id>/form/<pk>/dashboard', views.create_xform.as_view(), name="form_dashboard"),
    
    
    
    
]