from rest_framework import viewsets
from rest_framework import permissions, generics
from .serializers import ProjectSerializer, ProjectMembersSerializer
from accounts.serializers import UserSerializer
from projects.models import Project, ProjectMember, ProjectGroup
import operator
from django.db.models import Q
from functools import reduce
from django.contrib.auth.models import User, Group


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows projects to be viewed or edited.
    """
    queryset = Project.objects.all().order_by('-created_on')
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # get user
        cur_user        = self.request.user
        projects        = ProjectMember.objects.filter(member=cur_user).values_list('projectGroup__project_id', flat=True)
        return Project.objects.filter(pk__in=projects)


class ProjectMemberViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = ProjectMember.objects.all()
    serializer_class = ProjectMembersSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProjectMemberList(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        """
        This view should return a list of all the surveys for
        the project as determined by the project_id portion of the URL.
        """
        project_id  = self.kwargs['project_id']
        members     = ProjectMember.objects.filter(projectGroup__project_id=project_id).values_list('member', flat=True)
        return User.objects.filter(pk__in=members)



