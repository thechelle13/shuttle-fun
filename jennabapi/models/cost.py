from django.db import models
from .occurrence import Occurrence

class Cost(models.Model):
  
    
    label = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    occurrence = models.ForeignKey(Occurrence, on_delete=models.CASCADE, related_name="costs")