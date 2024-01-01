from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from jennabapi.models import Occurrence

class OccurrenceSerializer(serializers.ModelSerializer):
    
    #  def get_is_owner(self, obj):
    #     # Check if the authenticated user is the owner
    #     return self.context["request"].user == obj.shuttle_user.user
    
    # label
    
    class Meta:
        model = Occurrence
        fields = ["id", "label"]
    
class OccurrenceViewSet(viewsets.ViewSet):
    def list(self, request):
        occurrences = Occurrence.objects.all()
        serializer = OccurrenceSerializer(occurrences, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            occurrence = Occurrence.objects.get(pk=pk)
            serializer = OccurrenceSerializer(occurrence)
            return Response(serializer.data)
        
        except Occurrence.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)