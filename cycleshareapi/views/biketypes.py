"""View module for handling requests for states"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from cycleshareapi.models import Biketype 

class BikeTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for game types

    """
    class Meta:
        model = Biketype
        fields = ('id', 'label')

class BikeTypes(ViewSet):
    """CyCleShare biketypes"""


    def list(self, request):
        """Handle GET requests to get all biketypes

        Returns:
            Response -- JSON serialized list of biketypes
        """
        biketypes = Biketype.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = BikeTypeSerializer(
            biketypes, many=True, context={'request': request})
        return Response(serializer.data)
