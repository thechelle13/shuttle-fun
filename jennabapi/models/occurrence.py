from django.db import models


class Occurrence(models.Model):
  
    
    label = models.CharField(max_length=50)