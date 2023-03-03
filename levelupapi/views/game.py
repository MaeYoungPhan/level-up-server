"""View module for handling requests about game"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, Gamer, GameType


class GameView(ViewSet):
    """Level up game view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game
        """
        try:
            game = Game.objects.get(pk=pk) #make connection with server to return single query set where the primary key matches the pk requested by the client and assigns the object instance found to the game variable

            serializer = GameSerializer(game) #passes the instance stored in game through serializer to become a JSON stringified object and assigns it to serializer variable

            return Response(serializer.data, status=status.HTTP_200_OK) # returns serializer data to the client as a response. Response body is JSON stringified object of requested data.

        except Game.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all game

        Returns:
            Response -- JSON serialized list of game
        """
        # Make connection with server to retrieve a query set of all game items requested by client and assign the found instances to the game variable
        games = Game.objects.all()
        #passes instances stored in game variable to the serializer class to construct data into JSON stringified objects, which it then assigns to variable serializer
        serializer = GameSerializer(games, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK) #Constructs response and returns data requested by the client in the response body as an array of JSON stringified objects

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        gamer_id = Gamer.objects.get(user=request.auth.user) # connect with database and get user object based on token
        game_type = GameType.objects.get(pk=request.data["game_type"]) # connect with database to retrieve GameType object

        game = Game.objects.create(
            name=request.data["name"],
            gamer=gamer_id,
            game_type=game_type,
            max_players=request.data["max_players"]
        )
        serializer = GameSerializer(game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        game = Game.objects.get(pk=pk)
        game.name = request.data["name"]
        game.max_players = request.data["max_players"]

        game_type = GameType.objects.get(pk=request.data["game_type"])
        game.game_type = game_type
        game.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class GamerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gamer
        fields = ('id', )

class GameTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = GameType
        fields = ('id', 'type', )


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""
    # Converts meta data requested to JSON stringified object using Game as model
    gamer = GamerSerializer(many=False)
    game_type = GameTypeSerializer(many=False)
    class Meta: # configuration for serializer
        model = Game # model to use
        fields = ('id', 'name', 'gamer', 'game_type', 'max_players') # fields to include
