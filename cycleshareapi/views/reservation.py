"""View module for handling requests for reservations"""
from cycleshareapi.models.reservation import Reservation
from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from cycleshareapi.models import Rider, State, Bike, Biketype, Bikesize, Payment

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

class PaymentSerializer(serializers.ModelSerializer):
    """JSON serializer for payments

    """
    class Meta:
        model = Payment
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

class ReservationSerializer(serializers.ModelSerializer):
    """JSON serializer for reservations

    Arguments:
        serializer type
    """
    bike = BikeSerializer(many=False)
    payment = PaymentSerializer(many=False)
    rider = RiderSerializer(many=False)

    class Meta:
        model = Reservation
        fields = ('id', 'date', 'bike', 'payment', 'rider')

class MyReservations(ViewSet):
    """CyCleShare Payment Joins"""

    def list(self, request):       
        rider = Rider.objects.get(user = request.auth.user)
        reservations = Reservation.objects.filter(rider = rider)
        # reservations = Reservation.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = ReservationSerializer(
            reservations, many=True, context={'request': request})
        return Response(serializer.data)

    # def retrieve(self, request, pk=None):
    #     """Handle GET requests for single bike

    #     Returns:
    #         Response -- JSON serialized bike instance
    #     """
    #     try:
    #         mybike = Bike.objects.get(pk=pk)
    #         serializer = BikeSerializer(mybike, context={'request': request})
    #         return Response(serializer.data)
    #     except Exception as ex:
    #         return HttpResponseServerError(ex)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Reservation
        """

        # Uses the token passed in the `Authorization` header
        user = Rider.objects.get(pk=request.auth.user_id)

        # Create a new Python instance of the Game class
        # and set its properties from what was sent in the
        # body of the request from the client.
        reservation = Reservation()
        reservation.date = request.data["date"]
        reservation.bike = Bike.objects.get(pk=request.data["bikeId"])
        reservation.payment = Payment.objects.get(pk=request.data["paymentId"])
        reservation.rider = user

        # Try to save the new game to the database, then
        # serialize the game instance as JSON, and send the
        # JSON as a response to the client request
        try:
            reservation.save()
            serializer = ReservationSerializer(reservation, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    # def destroy(self, request, pk=None):
    #     """Handle DELETE requests for a single game

    #     Returns:
    #         Response -- 200, 404, or 500 status code
    #     """
    #     try:
    #         bike = Bike.objects.get(pk=pk)
    #         bike.delete()

    #         return Response({}, status=status.HTTP_204_NO_CONTENT)

    #     except Bike.DoesNotExist as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    #     except Exception as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)