"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import GameType


class GameTypeView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        game_type = GameType.objects.get(pk=pk) #make connection with server to return single query set where the primary key matches the pk requested by the client and assigns the object instance found to the game_type variable

        serializer = GameTypeSerializer(game_type) #passes the instance stored in game_type through serializer to become a JSON stringified object and assigns it to serializer variable

        return Response(serializer.data, status=status.HTTP_200_OK) # returns serializer data to the client as a response. Response body is JSON stringified object of requested data.


    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        # Make connection with server to retrieve a query set of all game types items requested by client and assign the found instances to the game_types variable
        game_types = GameType.objects.all()
        #passes instances stored in game_types variable to the serializer class to construct data into JSON stringified objects, which it then assigns to variable serializer
        serializer = GameTypeSerializer(game_types, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK) #Constructs response and returns data requested by the client in the response body as an array of JSON stringified objects

class GameTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for game types"""
    # Converts meta data requested to JSON stringified object using GameType as model
    class Meta: # configuration for serializer
        model = GameType # model to use
        fields = ('id', 'type') # fields to include
