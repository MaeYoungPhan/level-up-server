from django.db import models

class Event(models.Model):
    organizer = models.ForeignKey('Gamer', on_delete=models.CASCADE, related_name='gamer_id')
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    date = models.DateField(auto_now=False, auto_now_add=False)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    location = models.CharField(max_length=100)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    attendees = models.ManyToManyField("Gamer", through="EventAttendee", related_name='EventAttendees_gamer')
