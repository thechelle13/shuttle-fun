from django.db import models


class Cost(models.Model):
  
    
    label = models.CharField(max_length=50)
    price = models.DecimalField()
    