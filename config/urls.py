"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
import src.surveys.urls
from rest_framework import renderers

from rest_framework import routers
from src.accounts   import api as api_accounts
from src.projects   import api as api_projects
from src.surveys    import api as api_surveys

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = routers.DefaultRouter()
router.register(r'users', api_accounts.UserViewSet)
router.register(r'groups', api_accounts.GroupViewSet)
router.register(r'projects', api_projects.ProjectViewSet)
router.register(r'projectMembers', api_projects.ProjectMemberViewSet)
router.register(r'surveys', api_surveys.SurveyViewSet)
router.register(r'surveyQns', api_surveys.SurveyQuestionsViewSet)
router.register(r'surveyRsp', api_surveys.SurveyResponsesViewSet)
router.register(r'surveyFilters', api_surveys.SurveyFilterViewset)




urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path("survey/", include(src.surveys.urls)),
    path('submission',api_surveys.form_submission,name="form_submission"),



    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),



    path('formList',api_surveys.form_list, name="form_list"),
    path('formGet/<id>', api_surveys.form_get, name="form_get")
]
