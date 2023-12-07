from django.db import models

class Army(models.Model):
    name = models.CharField(max_length=250)
    image_url = models.URLField(null=True, blank=True)
    points = models.IntegerField(default=0)
    description = models.CharField(max_length=3000)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    user = models.ForeignKey('WargameUser', on_delete=models.CASCADE)