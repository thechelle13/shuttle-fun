from django.db import models

from .vehicle import Vehicle
from .client import Client


class Job(models.Model):


    shuttle_user = models.ForeignKey("ShuttleUser", on_delete=models.CASCADE, related_name="jobs")
    title = models.CharField(max_length=200)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="jobs")
    publication_date = models.DateField(auto_now_add=True)
    service_date = models.DateField()
    description = models.CharField(max_length=200)
    approved = models.BooleanField()
    distance = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    pay = models.DecimalField(max_digits=8, decimal_places=2)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="jobs")
   