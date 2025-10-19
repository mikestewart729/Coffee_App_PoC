from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import FavoriteShop
from .serializers import (
    CoffeeShopSerializer, FavoriteShopSerializer, 
    FavoriteShopCreateSerializer
)
from .services import GooglePlacesService

class NearbyShopsView(APIView):
    """
    Public endpoint to search for nearby coffee shops
    """
    def get(self, request): 
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')
        radius = request.GET.get('radius', 1600) # default to 1600 meteres, about 1 mile

        if not lat or not lng:
            return JsonResponse({
                'error': 'Missing required parameters: lat or lng'
            }, status=400)
        
        try:
            lat = float(lat)
            lng = float(lng)
            radius = int(radius)
        except ValueError:
            return JsonResponse({
                'error': 'Invalid parameter format: lat and lng must be float, radius must be int'
            }, status=400)
        
        try: 
            shops = GooglePlacesService.search_nearby_coffee_shops(lat, lng, radius)

            serializer = CoffeeShopSerializer(shops, many=True)

            return JsonResponse({
                'results': serializer.data,
                'count': len(serializer.data)
            }, status=200)
        except Exception as e:
            return JsonResponse({
                'error': 'Failed to fetch coffee shops',
                'message': str(e)
            }, status=500)

class FavoriteShopViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing a user's favorite coffee shops
    """
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return FavoriteShopCreateSerializer
        return FavoriteShopSerializer
    
    def get_queryset(self):
        return FavoriteShop.objects.filter(
            user=self.request.user
        ).select_related('shop').order_by('-favorited_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
