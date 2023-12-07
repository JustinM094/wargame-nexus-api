from django.db import models

class Game(models.Model):
    game_name = models.CharField(max_length=250)
    image_url = models.URLField(null=True, blank=True)
    description = models.CharField(max_length=3000)
    points = models.IntegerField(default=0)
    max_players = models.IntegerField(default=0)
    system = models.ForeignKey('System', on_delete=models.CASCADE)
    creator = models.ForeignKey('WargameUser', on_delete=models.CASCADE)