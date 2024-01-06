from .models import User
from rest_framework import serializers

class useSerilizers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email','first_name','status')