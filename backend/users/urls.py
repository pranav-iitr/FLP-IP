from django.urls import path, include
from rest_framework.routers import  SimpleRouter
from .views import *

# Create a router for the otp and verify ViewSets
auth_router = SimpleRouter()
org_user_router = SimpleRouter()
drone_router = SimpleRouter()
auth_router.register('otp',OTP_Router,basename='otp')
org_user_router.register('',org_router,basename='user')
drone_router.register('',drone_routes,basename='drone')

# auth_router.register('',SignUp_Router,basename='signup')
urlpatterns = [
    path('auth/', include(auth_router.urls)),
    path('org/', include(org_user_router.urls)),
    path('drone/', include(drone_router.urls)),
    path('retrive/',get_id.as_view())
]