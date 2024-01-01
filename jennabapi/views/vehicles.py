from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from jennabapi.models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    
    #  def get_is_owner(self, obj):
    #     # Check if the authenticated user is the owner
    #     return self.context["request"].user == obj.shuttle_user.user
    
    #  label, cost_id
    
    class Meta:
        model = Vehicle
        fields = ["id", "label", "cost_id"]
        
    
class VehicleViewSet(viewsets.ViewSet):
    def list(self, request):
        vehicles = Vehicle.objects.all()
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            vehicle = Vehicle.objects.get(pk=pk)
            serializer = VehicleSerializer(vehicle)
            return Response(serializer.data)
        
        except Vehicle.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def create(self, request):
        # Get the data from the client's JSON payload
        label = request.data.get("label")
        cost_id = request.data.get("cost_id")
      

        # Create a comment database row first, so you have a
        # primary key to work with
        vehicle = Vehicle.objects.create(
            
            label=label, 
            cost_id=cost_id,
       
        )

        serializer = VehicleSerializer(vehicle, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)