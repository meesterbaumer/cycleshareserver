"""View module for handling requests for states"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from cycleshareapi.models import Payment, Paymentjoin, Rider
from cycleshareapi.views.bike import RiderSerializer

class PaymentsSerializer(serializers.ModelSerializer):
    """JSON serializer for payments

    """
    class Meta:
        model = Payment
        fields = ('id', 'name')

class PaymentJoinsSerializer(serializers.ModelSerializer):
    """JSON serializer for payment joins

    """

    payment = PaymentsSerializer(many=False)
    rider = RiderSerializer(many=False)

    class Meta:
        model = Paymentjoin
        fields = ('id', 'payment', 'rider')

class Paymentjoins(ViewSet):
    """CyCleShare Payment Joins"""

    def list(self, request):
        """Handle GET requests to get all Payment Joins

        Returns:
            Response -- JSON serialized list of states
        """
        rider = Rider.objects.get(user = request.auth.user)
        # paymentjoins = Paymentjoin.objects.filter(rider = rider)
        paymentjoins = Paymentjoin.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = PaymentJoinsSerializer(
            paymentjoins, many=True, context={'request': request})
        return Response(serializer.data)
