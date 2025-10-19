# Django app for holding shop-related models. To include shop results from google maps
# API, cached search results, and User Favorite Shops.
from django.db import models
from django.utils import timezone

from api.models import User

class CoffeeShop(models.Model):
    """
    Model representing a coffee shop returned by the Google Places API (Legacy).
    """
    place_id = models.CharField(max_length=255, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    address = models.TextField()

    # Location
    latitude = models.FloatField()
    longitude = models.FloatField()

    # Some fields removed due to them being at enterprise API level only
    
    # Caching metadata
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta: 
        db_table = 'coffee_shops'
        indexes = [
            models.Index(fields=['latitude', 'longitude']),
            models.Index(fields=['last_updated']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.address}"
    
    def needs_refresh(self, hours=24):
        """
        Check if the cache data is stale
        """
        return (timezone.now() - self.last_updated).total_seconds() > (hours * 3600)

class SearchCache(models.Model):
    """
    Model to cache search results to reduce API calls and thus costs and time.
    """
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius = models.IntegerField()

    # Cached results
    results = models.JSONField(default=list)

    # Cache metadata
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        db_table = 'search_cache'
        indexes = [
            models.Index(fields=['latitude', 'longitude', 'radius']),
            models.Index(fields=['expires_at']),
        ]

    def is_valid(self):
        """ 
        Check if the cache is still valid
        """
        return timezone.now() < self.expires_at
    
    @classmethod
    def get_cached_search(cls, lat, lng, radius, tolerance=100):
        lat_tolerance = tolerance / 111000  # roughly meters to degrees
        lng_tolerance = tolerance / (111000 * abs(lat)) if lat != 0 else tolerance / 111000
        
        return cls.objects.filter(
            latitude__range=(lat - lat_tolerance, lat + lat_tolerance),
            longitude__range=(lng - lng_tolerance, lng + lng_tolerance),
            radius=radius,
            expires_at__gt=timezone.now()
        ).first() # Think through if I only want the first result or all?
    
class FavoriteShop(models.Model):
    """
    User's favorite coffee shops with custom ratings
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    shop = models.ForeignKey(CoffeeShop, on_delete=models.CASCADE, related_name='favorited_by')
    
    # Custom ratings per the brief (1-5 scale)
    taste_rating = models.IntegerField(null=True, blank=True)
    vibe_rating = models.IntegerField(null=True, blank=True)
    service_rating = models.IntegerField(null=True, blank=True)

    # Visit tracking
    last_visited = models.DateTimeField(null=True, blank=True)
    visit_count = models.IntegerField(default=0)
    
    # Timestamps
    favorited_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'favorite_shops'
        unique_together = ['user', 'shop']
        indexes = [
            models.Index(fields=['user', '-favorited_at']),
            models.Index(fields=['user', '-last_visited']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.shop.name}"
    
    # Calculate the overall rating based on user's three category ratings
    @property
    def overall_rating(self):
        """Calculate average rating across all categories"""
        ratings = [
            r 
            for r in [self.taste_rating, self.vibe_rating, self.service_rating] 
            if r is not None
        ]
        return sum(ratings) / len(ratings) if ratings else None
    
    # Method to track visits. Think about whether or not to implement
    def record_visit(self):
        """Update visit tracking"""
        self.last_visited = timezone.now()
        self.visit_count += 1
        self.save()