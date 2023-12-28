from .models import team_member
from rest_framework import serializers

class team_memberSerializer(serializers.ModelSerializer):
    class Meta:
        model = team_member
        excclude = ( 'created_at', 'updated_at')