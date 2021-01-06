"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from cycleshareapi.models import Rider, State, Bike, Biketype, Bikesize
import uuid
import base64
from django.core.files.base import ContentFile

class BikeOwnerSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer's related Django user"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class BikeTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for riders

    Arguments:
        serializer type
    """
    class Meta:
        model = Biketype
        fields = ('id', 'label')
        depth = 1

class BikeSizeSerializer(serializers.ModelSerializer):
    """JSON serializer for riders

    Arguments:
        serializer type
    """
    class Meta:
        model = Bikesize
        fields = ('id', 'label')
        depth = 1

class StateSerializer(serializers.ModelSerializer):
    """JSON serializer for game types

    """
    class Meta:
        model = State
        fields = ('id', 'name')

class RiderSerializer(serializers.ModelSerializer):
    """JSON serializer for riders

    Arguments:
        serializer type
    """
    user = BikeOwnerSerializer(many=False)
    state = StateSerializer(many=False)

    class Meta:
        model = Rider
        fields = ('id', 'user', 'address', 'city', 'image', 'state')
        depth = 1

class BikeSerializer(serializers.ModelSerializer):
    """JSON serializer for riders

    Arguments:
        serializer type
    """
    biketype = BikeTypeSerializer(many=False)
    bikesize = BikeSizeSerializer(many=False)
    rider = RiderSerializer(many=False)

    class Meta:
        model = Bike
        fields = ('id', 'year', 'make', 'model', 'image', 'fee', 'biketype', 'bikesize', 'rider')
        # depth = 1


class Bikes(ViewSet):
    """CyCleShare Bikes"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Rider
        """

        # Uses the token passed in the `Authorization` header
        user = Rider.objects.get(pk=request.auth.user_id)

        # Create a new Python instance of the Game class
        # and set its properties from what was sent in the
        # body of the request from the client.
        bike = Bike()
        bike.rider = user
        bike.year = request.data["year"]
        bike.make = request.data["make"]
        bike.model = request.data["model"]
        bike.fee = request.data["fee"]
        bike.biketype = Biketype.objects.get(pk=request.data["biketype"])
        bike.bikesize = Bikesize.objects.get(pk=request.data["bikesize"])
        bike.image = request.data["image"]

        if request.data["image"] is not None:
            format, imgstr = request.data["image"].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'"image"-{uuid.uuid4()}.{ext}')
            bike.image = data
        else: bike.image = "images/bikepics/image-2c93af49-3fe8-4ac4-9e43-8290153d65b4.jpeg"

        # Try to save the new game to the database, then
        # serialize the game instance as JSON, and send the
        # JSON as a response to the client request
        try:
            bike.save()
            serializer = BikeSerializer(bike, context={'request': request})
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
            bike = Bike.objects.get(pk=pk)
            serializer = BikeSerializer(bike, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for an updated Bike

        Returns:
            Response -- Empty body with 204 status code
        """
        user = Rider.objects.get(pk=request.auth.user_id)

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Bike, get the bike record
        # from the database whose primary key is `pk`
        bike = Bike.objects.get(pk=pk)
        bike.rider = user
        bike.year = request.data["year"]
        bike.make = request.data["make"]
        bike.model = request.data["model"]
        bike.fee = request.data["fee"]
        bike.biketype = Biketype.objects.get(pk=request.data["biketype"])
        bike.bikesize = Bikesize.objects.get(pk=request.data["bikesize"])

        bike.save()

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
        
        bikes = Bike.objects.all()

        serializer = BikeSerializer(
            bikes, many=True, context={'request': request})
        return Response(serializer.data)

