from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'location_lat', 'location_lng', 'default_search_radius']
        read_only_fields = ['id']
        extra_kwargs = {'password': {'write_only': True}}