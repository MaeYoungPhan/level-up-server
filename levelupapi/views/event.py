"""View module for handling requests about event"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Gamer, Game


class EventView(ViewSet):
    """Level up event view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized event
        """
        event = Event.objects.get(pk=pk) #make connection with server to return single query set where the primary key matches the pk requested by the client and assigns the object instance found to the event variable

        serializer = EventSerializer(event) #passes the instance stored in event through serializer to become a JSON stringified object and assigns it to serializer variable

        return Response(serializer.data, status=status.HTTP_200_OK) # returns serializer data to the client as a response. Response body is JSON stringified object of requested data.


    def list(self, request):
        """Handle GET requests to get all event

        Returns:
            Response -- JSON serialized list of event
        """
        # Make connection with server to retrieve a query set of all event items requested by client and assign the found instances to the event variable
        events = Event.objects.all()
        game = self.request.query_params.get('game')

        if game is not None:
            events = events.filter(game_id=game)
        
        else:
            pass

        #passes instances stored in event variable to the serializer class to construct data into JSON stringified objects, which it then assigns to variable serializer
        serializer = EventSerializer(events, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK) #Constructs response and returns data requested by the client in the response body as an array of JSON stringified objects

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        gamer_id = Gamer.objects.get(user=request.auth.user) # connect with database and get user object based on token
        game_id = Game.objects.get(pk=request.data["game"]) # connect with database to retrieve Game object

        event = Event.objects.create(
            organizer=gamer_id,
            name=request.data["name"],
            description=request.data["description"],
            date=request.data["date"],
            time=request.data["time"],
            location=request.data["location"],
            game=game_id
        )
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events"""
    # Converts meta data requested to JSON stringified object using Event as model
    class Meta: # configuration for serializer
        model = Event # model to use
        fields = ('id', 'organizer', 'name', 'description', 'date', 'time', 'location', 'game') # fields to include
