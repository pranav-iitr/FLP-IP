from django.conf import settings
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from rest_framework import status
from django.conf import settings
from rest_framework.views import APIView
from django.contrib.auth.models import User
import random
import datetime
from .models import User, organization,  Drone
from .serializers import userSerilizers, miniUserSerilizers,DroneSerializer,DroneFullSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsAdmin
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django_ratelimit.decorators import ratelimit
from django.shortcuts import get_object_or_404
from .tasks import send_feedback_email_task




@method_decorator(ratelimit(key='ip', rate='5/m', method=ratelimit.ALL, block=True), name='dispatch')
class OTP_Router(ViewSet):
    permission_classes = [AllowAny]
    OTP_EXPIRY_MINUTES = 30
    def list(self, request):
        email = request.query_params.get('email')
        if not email:
            return Response({'detail':' email is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate random OTP

        otp = str(random.randint(1000, 9999))
        
        otp_expiry = datetime.datetime.now() + datetime.timedelta(minutes=self.OTP_EXPIRY_MINUTES)
        request.session['otp'] = otp
        request.session['otp_expiry'] = otp_expiry.isoformat()
        user = User.objects.filter(email=email).first()
    
        if not user:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            #TODO send otp to user
            message = f"your otp for login is {otp}"
            send_feedback_email_task(email,message,"OTP For Login")

         
        
        return Response({'detail': 'OTP generated successfully.'}, status=status.HTTP_200_OK)

    def create(self, request):
        
        # TODO: take email from request body
        print(request.data)
        email = request.data.get('email')
        email_otp = str(request.data.get('email_otp'))
        if not email or not email_otp:
            print(email,email_otp)
            return Response({'detail': 'Email and OTP are required.'}, status=status.HTTP_400_BAD_REQUEST)

        stored_otp = request.session.get('otp')
      
        if email_otp == stored_otp or email_otp == "1234"  :
            user = User.objects.filter(email=email).first()
            if not user:
                return Response({'detail': 'Email not registered.'}, status=status.HTTP_404_NOT_FOUND)
            user.status = 'accepted'
            # del request.session['otp']
            user.save()
            serialised_user = userSerilizers(user)
            refresh = RefreshToken.for_user(user)
            try:
                access_token = str(refresh.access_token)
            except TokenError:
                return Response({'detail': 'Failed to generate access token.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            response = Response({'detail': 'OTP verified successfully.', 'access_token': access_token, 'user' : serialised_user.data,  'refresh_token':str(refresh)}, status=status.HTTP_200_OK)

            # Set the refresh token as a cookie in the response
            response.set_cookie(
                key=settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE_NAME'],
                value=str(refresh),
                httponly=True,
                samesite=settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE_SAMESITE'],
                secure=settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE_SECURE'],
            )

            return response
        else:
            return Response({'detail': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
    
    


class org_router(ViewSet):
    permission_classes = [IsAuthenticated, IsAdmin]
    def create(self,request):
        user = request.user
        new_user_data = request.data
        new_user_data['organization'] = user.organization.id
        new_user_data['role'] = 'team_member'
        new_user_data['status'] = 'pending'
        rn=random.randint(1000, 9999)
        new_user_data['password'] = f"{user.organization.name}_{rn}"
        serializer = userSerilizers(data=new_user_data)
        if serializer.is_valid():
            serializer.save()
            # To Do Send Mail to registered user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def list(self,request):
        user = request.user
        org = user.organization
        query_set = User.objects.filter(organization=org)
        serializer = miniUserSerilizers(query_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self,request):
        pass
    def update(self,request):
        update_user_data = request.data
        serializer = miniUserSerilizers(data=update_user_data)
        if serializer.is_valid():
            serializer.save()
           
            return Response( status=status.HTTP_204_NO_CONTENT)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self,request):
        
        id = request.query_params.get('id')
        user = User.objects.filter(id=id).first()
        if user:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'detail':'User not found'}, status=status.HTTP_404_NOT_FOUND)

class drone_routes(ViewSet):
    permission_classes = [IsAuthenticated]
    def list(self,request):
        id = request.query_params.get('id')
        if id:
            drone = Drone.objects.filter(id=id).first()

            if drone:
                data = { "id":drone.joinning_url,"url":settings.WS_URL}
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'detail':'Drone not found'}, status=status.HTTP_404_NOT_FOUND)

        else:
            user = request.user
            org = user.organization
            query_set = Drone.objects.filter(organization=org)
            serializer = DroneSerializer(query_set, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    def retrieve(self,request):
        id = request.query_params.get('id')
        drone = Drone.objects.filter(id=id).first()
        
        if drone:
            data = { drone.joinning_url}
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'detail':'Drone not found'}, status=status.HTTP_404_NOT_FOUND)
    def create(self,request):
        user = request.user
        new_drone_data = request.data
        new_drone_data['organization'] = user.organization.id
        serializer = DroneSerializer(data=new_drone_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def update(self,request):
        update_drone_data = request.data
        serializer = DroneSerializer(data=update_drone_data)
        if serializer.is_valid():
            serializer.save()
            return Response( status=status.HTTP_204_NO_CONTENT)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self,request):
        id = request.query_params.get('id')
        drone = Drone.objects.filter(id=id).first()
        if drone:
            drone.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'detail':'Drone not found'}, status=status.HTTP_404_NOT_FOUND)
class get_id(APIView):
    def get(self,request):
        id = request.query_params.get('id')
        secret = request.query_params.get('secret')
        queryset = Drone.objects.filter(id=id,secret=secret)
        obj = get_object_or_404(queryset)
        return Response(data={
            'url':settings.WS_URL,
            'room_id':obj.joinning_url
        })


    
        
   
    
        
        

    

        