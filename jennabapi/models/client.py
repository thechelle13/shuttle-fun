from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=100)
    service_date = models.DateField()
    fee = models.DecimalField(max_digits=10, decimal_places=2)