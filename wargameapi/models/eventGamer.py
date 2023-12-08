from django.db import models

class EventGamer(models.Model):
    user = models.ForeignKey('WargameUser', on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    army = models.OneToOneField('Army', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=None)