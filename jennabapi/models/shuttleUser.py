from django.db import models
from django.contrib.auth.models import User

class ShuttleUser(models.Model):

    bio = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="shuttle_user")