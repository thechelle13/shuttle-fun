from django.db import models


class Vehicle(models.Model):
  
    
    label = models.CharField(max_length=50)
 