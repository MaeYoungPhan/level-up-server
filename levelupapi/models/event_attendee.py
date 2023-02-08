from django.db import models

class EventAttendee(models.Model):
    gamer = models.ForeignKey('Gamer', on_delete=models.CASCADE, related_name='gamer_events')
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='event_attendees')
