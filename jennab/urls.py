"""
URL configuration for jennab project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from jennabapi.views import (
    ClientViewSet,
    UserViewSet,
    JobViewSet,
    CostViewSet,
    OccurrenceViewSet,
    VehicleViewSet,
    
)

router = DefaultRouter(trailing_slash=False)
router.register(r"clients", ClientViewSet, basename="client")
router.register(r"costs", CostViewSet, basename="costs")
router.register(r"vehicles", VehicleViewSet, basename="vehicles")
router.register(r"users", UserViewSet, basename="users")
router.register(r"users/shuttleusers", UserViewSet, basename="shuttleusers")
router.register(r"jobs", JobViewSet, basename="jobs")
router.register(r"occurrences", OccurrenceViewSet, basename="occurrences")

urlpatterns = [
    path("", include(router.urls)),
    path("login", UserViewSet.as_view({"post": "user_login"}), name="login"),
    path(
        "register", UserViewSet.as_view({"post": "register_account"}), name="register"
    ),
]