from django.urls import path
from django.conf.urls import url

from . import views, authentication
from . import ajax_datatable_views

#app_name = "ui"

urlpatterns = [
    path("", authentication.LoginView.as_view(), name="login"),
    path("logout", authentication.LogoutView.as_view(), name="logout"),
    path("dashboard", views.DashboardView.as_view(), name="dashboard"),

    path('ajax_datatable/permissions/', ajax_datatable_views.PermissionAjaxDatatableView.as_view(), name="ajax_datatable_permissions"),
    path('ajax_datatable/survey_list/', ajax_datatable_views.SurveyList.as_view(), name="surveylist"),
    path('ajax_datatable/project_member_list/', ajax_datatable_views.projectMemberslist.as_view(), name="projectMemberslist"),
    path('ajax_datatable/project_list/', ajax_datatable_views.ProjectList.as_view(), name="projectList"),
    path('ajax_datatable/form_data/', ajax_datatable_views.formData.as_view(), name="formData"),
    path('ajax_datatable/form_mapping/', ajax_datatable_views.FormMappingList.as_view(), name="FormMappingList"),
    
    #start
    # path('tutorial', views.list.as_view(), name="tutorial"),
    # path('case_studies', views.list_projects.as_view(), name="case_studies"),
    # path('awknolegements', views.list_projects.as_view(), name="awknoledgement"),
    
    #Projects
    path('project/dashboard', views.ProjectListView.as_view(), name="project_dashboard"),
    path('projects/lists', views.ProjectListView.as_view(), name="list_projects"),
    path('projects/create', views.ProjectCreateView.as_view(), name="create_project" ),
    
    path('project/<str:pk>', views.ProjectDetailView.as_view(), name="project_detail"),
    path('project/<pk>/groups', views.ProjectDetailView.as_view(), name="list_groups"),
    path('project/<pk>/members', views.ProjectDetailView.as_view(), name="list_members"),
    path('member/manage/<int:pk>', views.manage_project_member, name="manage_members"), 
    path('project/<pk>/form/create', views.create_xform.as_view(), name="create_xform"),
    
    
    # Form
    path('project/<int:project_id>/form/<pk>/data', views.form_data.as_view(), name="form_data"),
    
    path('form_data/<pk>', views.form_data_list, name="form_data_list"),
   #path('form_instance/<pk>', views.data_instance_wrp.as_view(), name="data_instance"),
    
    path('project/<int:project_id>/form/<pk>/map', views.create_xform.as_view(), name="form_map"),
    path('project/<int:project_id>/form/<pk>/mapping', views.form_mapping.as_view(), name="form_mapping"),
    path('project/<int:project_id>/form/<pk>/chart', views.create_xform.as_view(), name="form_chart"),
    path('project/<int:project_id>/form/<pk>/dashboard', views.create_xform.as_view(), name="form_dashboard"),
    
    
    
    # Instance
    path('instance/<pk>',views.data_instance_wrp.as_view(), name="instance"),
    path('form/chat',views.data_chat.as_view(), name="chat"),
    
    path('instance/data/<pk>', views.instance_data, name="instance_data"),
    path('instance/msg/<pk>', views.instance_messages, name="instance_messages"),
    path('instance/loc/<pk>', views.instance_location, name="instance_location"),
    path('instance/med/<pk>', views.instance_media, name="instance_media"),
    
    
    # form mapping
    path('form/mapping/<int:pk>',views.SurveyQuestionsUpdateView.as_view(), name="update_mapping"),
    
    
    
    
]