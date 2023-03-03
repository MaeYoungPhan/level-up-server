import json
from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import Event, Game, Gamer, EventAttendee
from rest_framework.authtoken.models import Token


class EventTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['users', 'tokens', 'gamers', 'game_types', 'games', 'events']

    def setUp(self):
        self.gamer = Gamer.objects.first()
        token = Token.objects.get(user=self.gamer.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_event(self):
        """
        Ensure we can create a new event.
        """
        # Define the endpoint in the API to which
        # the request will be sent
        url = "/events"

        # Define the request body
        data = {
            "name": "game party",
            "description": "board game party",
            "date": "2024-02-22",
            "time": "16:00:00",
            "location": "house",
            "game": 1
        }

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the event was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["name"], "game party")
        self.assertEqual(json_response["description"], "board game party")
        self.assertEqual(json_response["date"], "2024-02-22")
        self.assertEqual(json_response["time"], "16:00:00")
        self.assertEqual(json_response["location"], "house")

    def test_get_event(self):
        """
        Ensure we can get an existing game.
        """

        # Seed the database with a game
        event = Event()
        event.organizer_id = 1
        event.name = "Chutes and Ladders"
        event.description = "board game party"
        event.date = "2024-01-01"
        event.time = "15:00:00"
        event.location = "pool"
        event.game_id = 1
        event.save()

        # Initiate request and store response
        response = self.client.get(f"/events/{event.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the event was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["name"], "Chutes and Ladders")
        self.assertEqual(json_response["description"], "board game party")
        self.assertEqual(json_response["date"], "2024-01-01")
        self.assertEqual(json_response["time"], "15:00:00")
        self.assertEqual(json_response["location"], "pool")

    def test_change_event(self):
        """
        Ensure we can change an existing event.
        """
        event = Event()
        event.organizer_id = 1
        event.name = "Chutes and Ladders"
        event.description = "board game party"
        event.date = "2024-01-01"
        event.time = "15:00:00"
        event.location = "pool"
        event.game_id = 1
        event.save()

        # DEFINE NEW PROPERTIES FOR EVENT
        data = {
            "organizer": 1,
            "name": "game party",
            "description": "board game party",
            "date": "2024-01-01",
            "time": "16:00:00",
            "location": "house",
            "game": 1
        }

        response = self.client.put(f"/events/{event.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET event again to verify changes were made
        response = self.client.get(f"/events/{event.id}")
        json_response = json.loads(response.content)

        # Assert that the properties are correct
        self.assertEqual(json_response["name"], "game party")
        self.assertEqual(json_response["description"], "board game party")
        self.assertEqual(json_response["date"], "2024-01-01")
        self.assertEqual(json_response["time"], "16:00:00")
        self.assertEqual(json_response["location"], "house")

    def test_delete_event(self):
        """
        Ensure we can delete an existing event.
        """
        event = Event()
        event.organizer_id = 1
        event.name = "Chutes and Ladders"
        event.description = "board game party"
        event.date = "2024-01-01"
        event.time = "15:00:00"
        event.location = "pool"
        event.game_id = 1
        event.save()

        # DELETE the game you just created
        response = self.client.delete(f"/events/{event.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the event again to verify you get a 404 response
        response = self.client.get(f"/events/{event.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_signup_leave_event(self):
        """
        Ensure we can add/remove an gamer from event attendees using signup and leave custom actions.
        """

        event = Event()
        event.organizer_id = 1
        event.name = "Chutes and Ladders"
        event.description = "board game party"
        event.date = "2024-01-01"
        event.time = "15:00:00"
        event.location = "pool"
        event.game_id = 1
        event.save()

        gamer = 1

        event.attendees.add(gamer)

        # Initiate request and store response
        response = self.client.post(f"/events/{event.id}/signup")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the attendee was added to event
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["message"],"Gamer added")

        # DELETE the gamer sign up you just created
        response = self.client.delete(f"/events/{event.id}/leave")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
