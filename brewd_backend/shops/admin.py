from django.contrib import admin
from .models import CoffeeShop, FavoriteShop, SearchCache


@admin.register(CoffeeShop)
class CoffeeShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'last_updated']
    search_fields = ['name', 'address']


@admin.register(FavoriteShop)
class FavoriteShopAdmin(admin.ModelAdmin):
    list_display = ['user', 'shop', 'taste_rating', 'vibe_rating', 'service_rating', 'favorited_at']
    list_filter = ['taste_rating', 'vibe_rating', 'service_rating']


@admin.register(SearchCache)
class SearchCacheAdmin(admin.ModelAdmin):
    list_display = ['latitude', 'longitude', 'radius', 'created_at', 'expires_at']
