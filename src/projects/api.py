from rest_framework import viewsets
from rest_framework import permissions
from .serializers import ProjectSerializer, ProjectMembersSerializer
from projects.models import Project, ProjectMember, ProjectGroup
import operator
from django.db.models import Q
from functools import reduce


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
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




