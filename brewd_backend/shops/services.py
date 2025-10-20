# Services to handle Google Maps requests
import requests
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import CoffeeShop, SearchCache
import os
import math
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from a .env file if present
load_dotenv(os.path.join(BASE_DIR, '.env'))

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

class GooglePlacesService: 
    """Service for interacting with Google Places API (New)"""
    BASE_URL = 'https://places.googleapis.com/v1'

    @classmethod
    def _get_headers(cls):
        """Common headers for API requests"""
        return {
            'Content-Type': 'application/json',
            'X-Goog-Api-Key': GOOGLE_API_KEY,
            'X-Goog-FieldMask': 'places.id,places.displayName,places.formattedAddress,places.location'  
        }
    
    @classmethod
    def calculate_distance(cls, lat1, lng1, lat2, lng2):
        """
        Calculate distance between two points using Haversine formula
        Returns distance in meters
        """
        R = 6371000  # Earth's radius in meters
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lng = math.radians(lng2 - lng1)
        
        a = (math.sin(delta_lat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_lng / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        distance = R * c
        return distance
    
    @classmethod
    def format_distance(cls, distance_meters):
        """Format distance for display in miles"""
        distance_miles = distance_meters / 1609.34  # Convert meters to miles
        
        if distance_miles < 0.1:
            # For very short distances, show in feet
            distance_feet = distance_meters * 3.28084
            return f"{int(distance_feet)}ft"
        elif distance_miles < 1:
            # Show decimal for distances under 1 mile
            return f"{distance_miles:.2f}mi"
        else:
            # Show one decimal place for distances over 1 mile
            return f"{distance_miles:.1f}mi"
    
    @classmethod
    def search_nearby_coffee_shops(cls, lat, lng, radius=1500, use_cache=True):
        """
        Search for nearby coffee shops using Places API (New)
        Returns list of shops with distance information
        """
        if use_cache:
            cached_search = SearchCache.get_cached_search(lat, lng, radius)
            if cached_search and cached_search.is_valid():
                print(f"Using cached search results for lat={lat}, lng={lng}")
                shops = CoffeeShop.objects.filter(
                    place_id__in=cached_search.results
                )
                # Add distance to cached shops
                shops_with_distance = []
                for shop in shops:
                    distance = cls.calculate_distance(lat, lng, shop.latitude, shop.longitude)
                    shop.distance_meters = distance
                    shop.distance_formatted = cls.format_distance(distance)
                    shops_with_distance.append(shop)
                return shops_with_distance
        
        print(f"Fetching from Google Places API (New) for lat={lat}, lng={lng}")
        
        # New API uses POST with JSON body
        url = f'{cls.BASE_URL}/places:searchNearby'
        
        headers = cls._get_headers()
        
        body = {
            "includedTypes": ["cafe", "coffee_shop"],
            "maxResultCount": 20,
            "locationRestriction": {
                "circle": {
                    "center": {
                        "latitude": lat,
                        "longitude": lng
                    },
                    "radius": radius
                }
            }
        }
        
        response = requests.post(url, json=body, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Process results
        place_ids = []
        shops = []
        
        places = data.get('places', [])
        print(f"Found {len(places)} places")
        
        for place in places:
            shop = cls._cache_shop_data(place)
            
            # Calculate and add distance
            distance = cls.calculate_distance(lat, lng, shop.latitude, shop.longitude)
            shop.distance_meters = distance
            shop.distance_formatted = cls.format_distance(distance)
            
            shops.append(shop)
            place_ids.append(shop.place_id)
        
        # Sort by distance
        shops.sort(key=lambda x: x.distance_meters)
        
        # Cache the search
        if place_ids:
            SearchCache.objects.create(
                latitude=lat,
                longitude=lng,
                radius=radius,
                results=place_ids,
                expires_at=timezone.now() + timedelta(seconds=settings.SEARCH_CACHE_DURATION)
            )
        
        return shops
    
    @classmethod
    def _cache_shop_data(cls, place_data):
        """Store or update shop data from API result"""
        place_id = place_data.get('id')
        location = place_data.get('location', {})
        lat = location.get('latitude')
        lng = location.get('longitude')
        
        display_name = place_data.get('displayName', {})
        name = display_name.get('text', '') if isinstance(display_name, dict) else str(display_name)
        address = place_data.get('formattedAddress', '')
        
        shop, created = CoffeeShop.objects.update_or_create(
            place_id=place_id,
            defaults={
                'name': name,
                'address': address,
                'latitude': lat,
                'longitude': lng,
            }
        )
        
        action = "Created" if created else "Updated"
        print(f"{action} shop: {shop.name}")
        
        return shop