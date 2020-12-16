"""View module for handling requests for states"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from cycleshareapi.models import State


class States(ViewSet):
    """Level up game types"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        try:
            states = State.objects.get(pk=pk)
            serializer = StateSerializer(states, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        states = State.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = StateSerializer(
            states, many=True, context={'request': request})
        return Response(serializer.data)

class StateSerializer(serializers.ModelSerializer):
    """JSON serializer for game types

    """
    class Meta:
        model = State
        fields = ('id', 'name')