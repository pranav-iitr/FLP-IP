from .models import User, Drone
from rest_framework import serializers

class userSerilizers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email','first_name','status')


class miniUserSerilizers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','first_name','status','role','phone_no')
        extra_kwargs = {'password': {'write_only': True}}

class DroneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drone
        exclude = ('organization','joinning_url')
class DroneFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drone
        fields = '__all__'
        
        