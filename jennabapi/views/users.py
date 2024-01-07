from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from jennabapi.models import ShuttleUser




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "password", "first_name", "last_name", "email"]
        extra_kwargs = {"password": {"write_only": True}}
        
class ShuttleUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ShuttleUser
        fields = ("user", "active", "bio")
        
class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    @action(detail=False, methods=["get"], url_path="shuttleusers")
    def get_shuttle_users(self, request):
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return Response(
                {"error": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Filter ShuttleUser objects for the current authenticated user
        shuttle_user = ShuttleUser.objects.filter(user=request.user).first()

        # Check if the ShuttleUser exists
        if shuttle_user:
            serializer = ShuttleUserSerializer(shuttle_user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "ShuttleUser not found"}, status=status.HTTP_404_NOT_FOUND
            )
            
    def list(self, request):
        users = User.objects.all()  # Retrieve all users
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            user_instance = User.objects.get(pk=pk)
            serializer = UserSerializer(user_instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            user_instance = User.objects.get(pk=pk)

            # Is the authenticated user allowed to edit this user?
            self.check_object_permissions(request, user_instance)

            serializer = UserSerializer(user_instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()

                serialized_user = UserSerializer(
                    user_instance, context={"request": request}
                )
                return Response(serialized_user.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def destroy(self, request, pk=None):
        try:
            user_instance = User.objects.get(pk=pk)

            self.check_object_permissions(request, user_instance)

            user_instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=["post"], url_path="register")
    def register_account(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                # username=serializer.validated_data["username"],
                password=serializer.validated_data["password"],
                first_name=serializer.validated_data["first_name"],
                last_name=serializer.validated_data["last_name"],
                email=serializer.validated_data["email"],
                # email=serializer.validated_data["email"],
            )
            shuttle_user = ShuttleUser.objects.create(
                user=user,
                active=True,
                bio=request.data.get("bio"),
            )
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path="login")
    def user_login(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user:
            token = Token.objects.get(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST
            )
