from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from jennabapi.models import Client

class ClientSerializer(serializers.ModelSerializer):
    
    #  def get_is_owner(self, obj):
    #     # Check if the authenticated user is the owner
    #     return self.context["request"].user == obj.shuttle_user.user
    
    
    # name, service_date, fee
    
      class Meta:
        model = Client
        fields = ["id", "name", "fee", "service_date"]
        
class ClientViewSet(viewsets.ViewSet):
    def list(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            client = Client.objects.get(pk=pk)
            serializer = ClientSerializer(client)
            return Response(serializer.data)
        except Client.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        
    def create(self, request):
        # Get the data from the client's JSON payload
        name = request.data.get("name")
        fee = request.data.get("fee")
        service_date = request.data.get("service_date")

        # Create a comment database row first, so you have a
        # primary key to work with
        client = Client.objects.create(
            
            name=name, 
            fee=fee,
            service_date=service_date,
        )

        serializer = ClientSerializer(client, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)