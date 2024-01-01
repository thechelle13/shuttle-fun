from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from jennabapi.models import Cost


class CostSerializer(serializers.ModelSerializer):
    
    #  def get_is_owner(self, obj):
    #     # Check if the authenticated user is the owner
    #     return self.context["request"].user == obj.shuttle_user.user
    
    # type, price, occurrence
    
      class Meta:
        model = Cost
        fields = ["id", "label","price", "occurrence"]
        
class CostViewSet(viewsets.ViewSet):
    def list(self, request):
        costs = Cost.objects.all()
        serializer = CostSerializer(costs, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            cost = Cost.objects.get(pk=pk)
            serializer = CostSerializer(cost)
            return Response(serializer.data)
        except Cost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        
    def create(self, request):
        # Get the data from the client's JSON payload
        label = request.data.get("label")
        price = request.data.get("price")
        occurrence = request.data.get("occurrence")

        # Create a comment database row first, so you have a
        # primary key to work with
        cost = Cost.objects.create(
            
            label=label, 
            price=price,
            occurrence=occurrence,
        )

        serializer = CostSerializer(cost, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)