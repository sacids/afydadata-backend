from rest_framework import viewsets
from rest_framework import permissions
from .serializers import ProjectSerializer, ProjectMembersSerializer
from projects.models import Project, ProjectMembers


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Project.objects.all().order_by('-created_on')
    serializer_class = ProjectSerializer
    #permission_classes = [permissions.IsAuthenticated]


class ProjectMemberViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = ProjectMembers.objects.all()
    serializer_class = ProjectMembersSerializer
    #permission_classes = [permissions.IsAuthenticated]