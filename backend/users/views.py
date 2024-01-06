from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from rest_framework import status
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.auth import authenticate


from .models import User, organization, team_member, drone
from .serializers import useSerilizers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django_ratelimit.decorators import ratelimit
import re
import random
import datetime
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
        print(otp)
        # Store the generated OTP and its expiry timestamp in user's session
        otp_expiry = datetime.datetime.now() + datetime.timedelta(minutes=self.OTP_EXPIRY_MINUTES)
        request.session['otp'] = otp
        request.session['otp_expiry'] = otp_expiry.isoformat()
        user = User.objects.filter(email=email).first()
        print(user)
        if not user:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            #TODO send otp to user


            pass
        
        return Response({'detail': 'OTP generated successfully.'}, status=status.HTTP_200_OK)

    def create(self, request):
        
        # TODO: take email from request body
        email = request.data.get('email')
        email_otp = str(request.data.get('email_otp'))
        if not email or not email_otp:
            return Response({'detail': 'Email and OTP are required.'}, status=status.HTTP_400_BAD_REQUEST)

        stored_otp = request.session.get('otp')
        print("email: "+email + " stored otp: " + stored_otp + " email otp: " + email_otp)
        if email_otp == stored_otp :
            user = User.objects.filter(email=email).first()
            if not user:
                return Response({'detail': 'Email not registered.'}, status=status.HTTP_404_NOT_FOUND)
            user.status = 'accepted'
            del request.session['otp']
            user.save()
            serialised_user = useSerilizers(user)
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
    
class Signin(ViewSet):
    permission_classes = [AllowAny]
    def create(self, request):
        
        pass

        