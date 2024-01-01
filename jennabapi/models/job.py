from django.db import models

from .vehicle import Vehicle


class Job(models.Model):


    shuttle_user = models.ForeignKey("ShuttleUser", on_delete=models.CASCADE, related_name="jobs")
    title = models.CharField(max_length=200)
    client = models.CharField(max_length=30) 
    publication_date = models.DateField(auto_now_add=True)
    service_date = models.DateField()
    description = models.CharField(max_length=200)
    approved = models.BooleanField()
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="jobs")
    # costs = models.ManyToManyField("Cost", through="VehicleCost", related_name="jobs")