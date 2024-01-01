from django.db import models



class VehicleCost(models.Model):
   

    cost = models.ForeignKey("Cost", on_delete=models.CASCADE, related_name="vehicle_costs")
    vehicle = models.ForeignKey("Vehicle", on_delete=models.CASCADE, related_name="vehicle_costs" )