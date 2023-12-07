from django.contrib.auth.models import User
from django.db import models

class WargameUser(models.Model):
    bio = models.CharField(max_length=3000)
    profile_image_url = models.URLField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wargame_username = models.CharField(max_length=65)