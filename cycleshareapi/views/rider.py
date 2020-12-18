"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from cycleshareapi.models import Rider, State
from django.contrib.auth.models import User

class Riders(ViewSet):
    """CyCleShare Riders"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Rider
        """

        # Uses the token passed in the `Authorization` header
        user = User.objects.get(pk=request.auth.user_id)

        # Create a new Python instance of the Game class
        # and set its properties from what was sent in the
        # body of the request from the client.
        rider = Rider()
        rider.user = user
        rider.address = request.data["address"]
        rider.city = request.data["city"]
        rider.state = State.objects.get(pk=request.data["state"])

        # Try to save the new game to the database, then
        # serialize the game instance as JSON, and send the
        # JSON as a response to the client request
        try:
            rider.save()
            serializer = RiderSerializer(rider, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/games/2
            #
            # The `2` at the end of the route becomes `pk`
            rider = Rider.objects.get(pk=pk)
            serializer = RiderSerializer(rider, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        rider = Rider.objects.get(user=request.auth.user)

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Game, get the game record
        # from the database whose primary key is `pk`
        rider = Rider.objects.get(pk=pk)
        rider.user = rider
        rider.address = request.data["address"]
        rider.city = request.data["city"]
        rider.state = request.data["state"]

        rider.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            rider = Rider.objects.get(pk=pk)
            rider.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Rider.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to games resource

        Returns:
            Response -- JSON serialized list of games
        """
        # Get all game records from the database
        riders = Rider.objects.all()

        serializer = RiderSerializer(
            riders, many=True, context={'request': request})
        return Response(serializer.data)

class RiderSerializer(serializers.ModelSerializer):
    """JSON serializer for riders

    Arguments:
        serializer type
    """
    class Meta:
        model = Rider
        fields = ('id', 'address', 'city', 'image', 'state')
        depth = 1
