from rest_framework import serializers
from projects.models import Project, ProjectMember


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project # this is the model that is being serialized
        fields = ('title', 'description','created_by','created_on')

class ProjectMembersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProjectMember # this is the model that is being serialized
        fields = ('projectGroup', 'member')