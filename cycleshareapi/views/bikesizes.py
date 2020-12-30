"""View module for handling requests for states"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from cycleshareapi.models import Bikesize 

class BikeSizeSerializer(serializers.ModelSerializer):
    """JSON serializer for Bike Sizes

    """
    class Meta:
        model = Bikesize
        fields = ('id', 'label')

class BikeSizes(ViewSet):
    """CyCleShare bikesizes"""


    def list(self, request):
        """Handle GET requests to get all bikesizes

        Returns:
            Response -- JSON serialized list of bikesizes
        """
        bikesizes = Bikesize.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = BikeSizeSerializer(
            bikesizes, many=True, context={'request': request})
        return Response(serializer.data)
