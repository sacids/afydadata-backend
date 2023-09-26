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
    path('ajax_datatable/project_group_list/', ajax_datatable_views.projectGrouplist.as_view(), name="projectGroupList"),
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
    path('project/delete/<str:pk>', views.ProjectDeleteView.as_view(), name="delete_project"),
    path('project/<pk>/groups', views.ProjectDetailView.as_view(), name="list_groups"),
    path('project/<pk>/members', views.ProjectDetailView.as_view(), name="list_members"),

    #project surveys
    path('project/<str:pk>/form/create', views.XformCreateView.as_view(), name="create_xform"),
    #path('project/<str:pk>/form/delete', views.XformDeleteView.as_view(), name="delete_xform"),
    
    # project members
    path('member/manage/<str:pk>', views.manage_project_member, name="manage_members"),
    path('project/<str:pk>/member/create', views.MemberCreateView.as_view(), name="create_member"),
    path('member/manage/<str:pk>/manage_profile', views.ManagePmGroups.as_view(), name="manage_pm_profile"),
    path('member/change_password/<pk>', views.ChangePmPassword.as_view(), name="change_pm_password"),
    path('member/manage_access/<str:pk>', views.MembersPermsView.as_view(), name="manage_members_access"),
    
    path('update_members_access/<str:pk>', views.update_members_access, name="update_members_access"),

    # project groups
    path('project/group/manage/<str:pk>', views.manage_project_group, name="manage_project_group"),
    path('project/<str:project_id>/group/create', views.GroupCreateView.as_view(), name="create_group"),
    path('project/group/edit/<str:pk>', views.EditGroupView.as_view(), name="edit_group"),
    path('member/manage/<str:pk>/manage_group', views.ManagePmGroups.as_view(), name="manage_pm_groups"),

    # project surveys data
    path('project/<str:project_id>/form/<str:pk>/data', views.FormDataView.as_view(), name="form_data"),
    path('project/<str:project_id>/form/<pk>/mapping', views.FormMappingView.as_view(), name="form_mapping"),
    path('project/<str:project_id>/form/<pk>/perms', views.FormPermsView.as_view(), name="form_perms"),
    path('project/<str:project_id>/form/<pk>/chart', views.FormMapView.as_view(), name="form_chart"),
    path('project/<str:project_id>/form/<pk>/map', views.FormMapView.as_view(), name="form_map"),
    path('project/<str:project_id>/form/<pk>/dashboard', views.FormMapView.as_view(), name="form_dashboard"),
    
    
    path('update_survey_access/<str:pk>', views.update_survey_access, name="update_survey_access"),
    
    
    
    path('form_data/<str:pk>', views.form_data_list, name="form_data_list"),
   #path('form_instance/<pk>', views.data_instance_wrp.as_view(), name="data_instance"),
    
    path('project/<str:project_id>/form/<pk>/show', views.manage_form_summary, name="manage_form_summary"),
    path('project/<str:project_id>/form/<pk>/map', views.form_summary_map.as_view(), name="form_summary_map"),    
    
    
    # Instance
    path('instance/<pk>',views.data_instance_wrp.as_view(), name="instance"),
    path('form/chat',views.data_chat.as_view(), name="chat"),
    
    path('instance/data/<pk>', views.instance_data, name="instance_data"),
    path('instance/msg/<pk>', views.instance_messages, name="instance_messages"),
    path('instance/msg/add', views.instance_messages_add, name="instance_messages_add"),
    path('instance/loc/<pk>', views.instance_location, name="instance_location"),
    path('instance/med/<pk>', views.instance_media, name="instance_media"),
    
    
    # form mapping
    path('form/mapping/<str:pk>',views.SurveyQuestionsUpdateView.as_view(), name="update_mapping"),
    
    
    # ajax functions
    
    
    
    
    
]