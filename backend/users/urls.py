from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import *

# Create a router for the otp and verify ViewSets
auth_router = SimpleRouter()
auth_router.register('otp',OTP_Router,basename='otp')
urlpatterns = [
    path('auth/', include(auth_router.urls)),
   
]