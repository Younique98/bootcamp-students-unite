"""View module for handling requests about group_projects"""
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth.models import User
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from bootcampstudentsuniteapi.models import BootCampGraduate, GroupProject, Participant as ParticipantModel


class GroupProjects(ViewSet):
    """Group Project"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized group_project instance
        """
        bootcamp_graduate = BootCampGraduate.objects.get(
            user=request.auth.user)
        # Uses the token passed in the `Authorization` header
        # bootcamp_graduate = GroupProject.objects.get(user=request.auth.user)

        # Create a new Python instance of the GroupProject class
        # and set its properties from what was sent in the
        # body of the request from the client.
        group_project = GroupProject()
        group_project.title = request.data["title"]
        group_project.number_of_graduates_signed_up = request.data["numberOfGraduatesSignedUp"]
        group_project.description = request.data["description"]
        group_project.estimated_time_to_completion = request.data["estimatedTimeToCompletion"]
        group_project.github_link = request.data["gitHubLink"]
        group_project.project_manager = bootcamp_graduate
        group_project.bootcamp_graduate = bootcamp_graduate

        # Use the Django ORM to get the record from the database
        # whose `id` is what the client passed as the
        # `categoryId` in the body of the request.

        # Try to save the new group_project to the database, then
        # serialize the group_project instance as JSON, and send the
        # JSON as a response to the client request
        try:
            group_project.save()

            serializer = GroupProjectSerializer(
                group_project, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single group_project

        Returns:
            Response -- JSON serialized group_project instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/group_projects/2
            #
            # The `2` at the end of the route becomes `pk`
            group_project = GroupProject.objects.get(pk=pk)
            serializer = GroupProjectSerializer(
                group_project, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a group_project

        Returns:
        Response -- Empty body with 204 status code
        """
        bootcamp_graduate = BootCampGraduate.objects.get(
            user=request.auth.user)

        group_project = GroupProject.objects.get(pk=pk)
        group_project.title = request.data["title"]
        group_project.number_of_graduates_signed_up = request.data["numberOfGraduatesSignedUp"]
        group_project.description = request.data["description"]
        group_project.estimated_time_to_completion = request.data["estimatedTimeToCompletion"]
        group_project.github_link = request.data["gitHubLink"]
        group_project.bootcamp_graduate = bootcamp_graduate

        # Use the Django ORM to get the record from the database
        # whose `id` is what the client passed as the
        # `categoryId` in the body of the request.

        group_project.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single group_project

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            group_project = GroupProject.objects.get(pk=pk)
            group_project.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except GroupProject.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['post', 'delete'], detail=True)
    def signup(self, request, pk=None):
        """Managing bootcamp_graduates signing up for group_projects"""

        # A bootcamp_graduate wants to sign up for an group_project
        if request.method == "POST":
            # The pk would be `2` if the URL above was requested
            group_project = GroupProject.objects.get(pk=pk)

            # Django uses the `Authorization` header to determine
            # which user is making the request to sign up
            bootcamp_graduate = BootCampGraduate.objects.get(
                user=request.auth.user)

            try:
                # Determine if the user is already signed up
                registration = ParticipantModel.objects.get(
                    group_project=group_project, bootcamp_graduate=bootcamp_graduate)
                return Response(
                    {'message': 'ParticipantModel is already signed up for this project.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except ParticipantModel.DoesNotExist:
                # The user is not signed up.
                registration = ParticipantModel()
                registration.group_project = group_project
                registration.bootcamp_graduate = bootcamp_graduate
                registration.save()

                return Response({}, status=status.HTTP_201_CREATED)

        # User wants to leave a previously joined group_project
        elif request.method == "DELETE":
            # Handle the case if the client specifies a group_project
            # that doesn't exist
            try:
                group_project = GroupProject.objects.get(pk=pk)
            except GroupProject.DoesNotExist:
                return Response(
                    {'message': 'Group Project does not exist.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Get the authenticated user
            bootcamp_graduate = BootCampGraduate.objects.get(
                user=request.auth.user)

            try:
                # Try to delete the signup
                registration = ParticipantModel.objects.get(
                    group_project=group_project, bootcamp_graduate=bootcamp_graduate)
                registration.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)

            except ParticipantModel.DoesNotExist:
                return Response(
                    {'message': 'Not currently following this group project.'},
                    status=status.HTTP_404_NOT_FOUND
                )

        # If the client performs a request with a method of
        # anything other than POST or DELETE, tell client that
        # the method is not supported
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request):
        """Handle GET requests to group_projects resource

        Returns:
            Response -- JSON serialized list of group_projects
        """
        # Get all group_project records from the database
        bootcamp_graduate = BootCampGraduate.objects.get(
            user=request.auth.user)
        group_projects = GroupProject.objects.all()

       # Set the `joined` property on every event
        for group_project in group_projects:
            group_project.joined = None

            try:
                ParticipantModel.objects.get(
                    group_project=group_project, bootcamp_graduate=bootcamp_graduate)
                group_project.joined = True
            except ObjectDoesNotExist:
                group_project.joined = False

        serializer = GroupProjectSerializer(
            group_projects, many=True, context={'request': request})
        return Response(serializer.data)


class GroupProjectUserSerializer(serializers.ModelSerializer):
    """JSON serializer for group project organizer's related Django user"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ParticipantSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer"""
    user = GroupProjectUserSerializer(many=False)

    class Meta:
        model = BootCampGraduate
        fields = ['user']


class GroupProjectSerializer(serializers.ModelSerializer):
    """JSON serializer for group_projects"""
    project_manager = ParticipantSerializer(many=False)

    class Meta:
        model = GroupProject
        fields = ('id', 'title', 'number_of_graduates_signed_up',  'description', 'project_manager', 'estimated_time_to_completion',
                  'github_link', 'project_manager')
