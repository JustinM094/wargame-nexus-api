from django.db import models

class Event(models.Model):
    event_name = models.CharField(max_length=150)
    event_location = models.CharField(max_length=150)
    event_time = models.DateTimeField(default=None)
    host = models.ForeignKey('WargameUser', on_delete=models.CASCADE)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
