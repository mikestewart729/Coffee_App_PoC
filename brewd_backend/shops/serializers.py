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
            'overall_rating', 'last_visited', 'visit_count',
            'favorited_at', 'updated_at'
        ]

class FavoriteShopCreateSerializer(serializers.ModelSerializer):
    shop_place_id = serializers.CharField(write_only=True)
    
    class Meta:
        model = FavoriteShop
        fields = [
            'shop_place_id', 'taste_rating', 'vibe_rating', 'service_rating'
        ]
    
    def create(self, validated_data):
        place_id = validated_data.pop('shop_place_id')
        user = self.context['request'].user
        
        # Get or create shop
        try:
            shop = CoffeeShop.objects.get(place_id=place_id)
        except CoffeeShop.DoesNotExist:
            raise serializers.ValidationError(
                "Shop not found. Please search for it first."
            )
        
        # Create or update favorite
        favorite, created = FavoriteShop.objects.update_or_create(
            user=user,
            shop=shop,
            defaults=validated_data
        )
        return favorite