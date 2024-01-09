from django.db import models


class Vehicle(models.Model):
  
    
    label = models.CharField(max_length=50)
    cost = models.ForeignKey("Cost", on_delete=models.CASCADE, related_name="costs")