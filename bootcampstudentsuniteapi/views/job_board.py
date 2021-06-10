"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.decorators import action
from bootcampstudentsuniteapi.models import JobBoard, BootCampGraduate


class JobBoards(ViewSet):
    """Job Board"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized job_board instance
        """
        bootcamp_graduate = BootCampGraduate.objects.get(
            user=request.auth.user)
        # Uses the token passed in the `Authorization` header
        # bootcamp_graduate = JobBoard.objects.get(user=request.auth.user)

        # Create a new Python instance of the JobBoard class
        # and set its properties from what was sent in the
        # body of the request from the client.
        job_board = JobBoard()
        job_board.title = request.data["title"]
        job_board.description = request.data["description"]
        job_board.job_link = request.data["jobLink"]
        job_board.poster = bootcamp_graduate
        job_board.bootcamp_graduate = bootcamp_graduate

        # Use the Django ORM to get the record from the database
        # whose `id` is what the client passed as the
        # `categoryId` in the body of the request.

        # Try to save the new job_board to the database, then
        # serialize the job_board instance as JSON, and send the
        # JSON as a response to the client request
        try:
            job_board.save()

            serializer = JobBoardSerializer(
                job_board, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single job_board

        Returns:
            Response -- JSON serialized job_board instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/jobboard/2
            #
            # The `2` at the end of the route becomes `pk`
            job_board = JobBoard.objects.get(pk=pk)
            serializer = JobBoardSerializer(
                job_board, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a job_board

        Returns:
        Response -- Empty body with 204 status code
        """
        bootcamp_graduate = BootCampGraduate.objects.get(
            user=request.auth.user)

        job_board = JobBoard.objects.get(pk=pk)
        job_board.title = request.data["title"]
        job_board.description = request.data["description"]
        job_board.job_link = request.data["jobLink"]
        job_board.poster = bootcamp_graduate
        job_board.bootcamp_graduate = bootcamp_graduate

        # Use the Django ORM to get the record from the database
        # whose `id` is what the client passed as the
        # `categoryId` in the body of the request.

        job_board.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single job_board

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            job_board = JobBoard.objects.get(pk=pk)
            job_board.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except JobBoard.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to jobboards resource

        Returns:
            Response -- JSON serialized list of job_boards
        """
        # Get all job_board records from the database
        job_boards = JobBoard.objects.all()

        serializer = JobBoardSerializer(
            job_boards, many=True, context={'request': request})
        return Response(serializer.data)


class JobBoardUserSerializer(serializers.ModelSerializer):
    """JSON serializer for group project organizer's related Django user"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class JobBoardSerializer(serializers.ModelSerializer):
    """JSON serializer for job_boards"""

    class Meta:
        model = JobBoard
        fields = ('id', 'title', 'description', 'poster', 'job_link')
