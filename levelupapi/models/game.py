from django.db import models

class Game(models.Model):
    name = models.CharField(max_length=55)
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    game_type = models.ForeignKey("GameType", on_delete=models.CASCADE, null=True)
    max_players = models.IntegerField()
