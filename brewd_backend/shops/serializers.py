from rest_framework import serializers
from .models import CoffeeShop, FavoriteShop

class CoffeeShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoffeeShop
        fields = '__all__'

class FavoriteShopSerializer(serializers.ModelSerializer):
    shop = CoffeeShopSerializer(read_only=True)
    overall_rating = serializers.ReadOnlyField()
    
    class Meta:
        model = FavoriteShop
        fields = [
            'id', 'shop', 'taste_rating', 'vibe_rating', 'service_rating',
            'overall_rating', 'notes', 'last_visited', 'visit_count',
            'favorited_at', 'updated_at'
        ]

## Additional serializers can be added here as needed