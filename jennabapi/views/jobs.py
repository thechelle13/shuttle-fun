from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from jennabapi.models import Job, ShuttleUser, Client
from django.contrib.auth.models import User
from .users import ShuttleUserSerializer
from .clients import ClientSerializer

class SimpleJobSerializer(serializers.ModelSerializer):   
    # is_owner = serializers.SerializerMethodField()

    # def get_is_owner(self, obj):
    #     # Check if the authenticated user is the owner
    #     return self.context["request"].user == obj.tech_user.user

    class Meta:
        model = Job
        fields = [
            "shuttle_user",
            "title",
            "client",
            "publication_date",
            "service_date",
            "description",
            "approved",
            "distance",
            "vehicle",
            # "rate",
        ]

class JobSerializer(serializers.ModelSerializer):
    shuttle_user = ShuttleUserSerializer(many=False)
    is_owner = serializers.SerializerMethodField()
    client = ClientSerializer(many=False)

    def get_is_owner(self, obj):
        # Check if the authenticated user is the owner
        return self.context["request"].user == obj.shuttle_user.user

    class Meta:
        model = Job
        fields = [
            "id",
            "shuttle_user",
            "title",
            "client",
            "publication_date",
            "service_date",
            "description",
            "approved",
            "distance",
            "vehicle",
            # "rate",
            "is_owner",
        ]

class JobViewSet(viewsets.ViewSet):
    def list(self, request):
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True, context={"request": request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            job = Job.objects.get(pk=pk)
            serializer = JobSerializer(job, context={"request": request})
            return Response(serializer.data)

        except Job.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        # Get the data from the client's JSON payload
        shuttle_user = ShuttleUser.objects.get(user=request.auth.user)
        title = request.data.get("title")
        publication_date = request.data.get("publication_date")
        service_date = request.data.get("service_date")
        description = request.data.get("description")
        distance = request.data.get("distance")
        # rate = request.data.get("rate")
        approved = request.data.get("approved")
        vehicle = request.data.get("vehicle")
        client_id = request.data.get("client")
        client = Client.objects.get(pk=client_id)
       

        # Create a job database row first, so you have a
        # primary key to work with
        job = Job.objects.create(
            shuttle_user=shuttle_user,
            title=title,
            publication_date=publication_date,
            service_date=service_date,
            # rate=rate,
            description=description,
            approved=approved,
            client=client,
            vehicle=vehicle,
            distance=distance,
        )
        
        # Establish the many-to-many relationships if any
       

        serializer = JobSerializer(job, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:
            job = Job.objects.get(pk=pk)

            # Is the authenticated user allowed to edit this job?
            self.check_object_permissions(request, job)

            serializer = SimpleJobSerializer(data=request.data)
            if serializer.is_valid():
                
                job.title = serializer.validated_data["title"]
                job.publication_date = serializer.validated_data["publication_date"]
                job.service_date = serializer.validated_data["service_date"]
                job.client = serializer.validated_data["client"]
                job.description = serializer.validated_data["description"]
                job.approved = serializer.validated_data["approved"]
                job.distance = serializer.validated_data["distance"]
                job.vehicle = serializer.validated_data["vehicle"]
                # job.rate = serializer.validated_data["rate"]
                job.save()

                serializer = JobSerializer(job, context={"request": request})
                return Response(None, status.HTTP_204_NO_CONTENT)

            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except Job.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            job = Job.objects.get(pk=pk)
            self.check_object_permissions(request, job)
            job.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Job.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
