from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NearbyShopsView, FavoriteShopViewSet

router = DefaultRouter()
router.register(r'favorites', FavoriteShopViewSet, basename='favorite')

urlpatterns = [
    # Coffee shop search
    path('nearby/', NearbyShopsView.as_view(), name='nearby-shops'),
    
    # Favorites (from router)
    path('', include(router.urls)),
]