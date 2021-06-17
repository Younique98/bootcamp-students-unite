"""View module for handling requests about park areas"""
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from bootcampstudentsuniteapi.models import GroupProject, BootCampGraduate, Participant


class Profile(ViewSet):
    """BootCampGraduate can see profile information"""

    def list(self, request):
        """Handle GET requests to profile resource

        Returns:
            Response -- JSON representation of user info and group_project
        """
        bootcamp_graduate = BootCampGraduate.objects.get(
            user=request.auth.user)

        group_projects = GroupProject.objects.filter(
            participants=bootcamp_graduate
        )

        group_project = GroupProject.objects.all()

        group_projects = IndividualGroupProjectSerializer(
            group_projects, many=True, context={'request': request})

        group_project = GroupProjectSerializer(
            group_project, many=True, context={'request': request})

        bootcamp_graduate = BootCampGraduateSerializer(
            bootcamp_graduate, many=False, context={'request': request})

        # Manually construction of  the JSON structure in the response
        profile = {}
        profile["bootcamp_graduate"] = bootcamp_graduate.data
        profile["group_projects"] = group_projects.data
        profile["group_project"] = group_project.data

        return Response(profile)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for bootcamp_graduate's related Django user"""
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username')


class BootCampGraduateSerializer(serializers.ModelSerializer):
    """JSON serializer for bootcamp_graduates"""
    user = UserSerializer(many=False)

    class Meta:
        model = BootCampGraduate
        fields = ('id', 'user', 'bio', 'bootcamp_graduate_image')


class IndividualGroupProjectSerializer(serializers.ModelSerializer):
    """JSON serializer for group_project"""

    class Meta:
        model = GroupProject
        fields = ('id', 'title', 'number_of_graduates_signed_up',  'description', 'project_manager', 'estimated_time_to_completion',
                  'github_link', 'participants')


class GroupProjectSerializer(serializers.ModelSerializer):
    """JSON serializer for group_project"""

    class Meta:
        model = GroupProject
        fields = ('id', 'title', 'number_of_graduates_signed_up',  'description', 'project_manager', 'estimated_time_to_completion',
                  'github_link', 'participants')


class ParticipantSerializer(serializers.ModelSerializer):
    """JSON serializer for group_project"""

    class Meta:
        model = Participant
        fields = ('bootcamp_graduate', 'group_project')
