# Services to handle Google Maps requests
import requests
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import CoffeeShop, SearchCache
import os
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
    def search_nearby_coffee_shops(cls, lat, lng, radius=1600, use_cache=True):
        """
        Search for nearby coffee shops using Places API (New)
        """
        if use_cache:
            cached_search = SearchCache.get_cached_search(lat, lng, radius)
            if cached_search and cached_search.is_valid():
                print(f"Using cached search results for lat={lat}, lng={lng}")
                return CoffeeShop.objects.filter(
                    place_id__in=cached_search.results
                )
            
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
            shops.append(shop)
            place_ids.append(shop.place_id)
        
        # Cache the search results
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
        """
        Store or update shop data from API result
        New API has different structure than legacy
        """
        place_id = place_data.get('id')
        
        # Extract location
        location = place_data.get('location', {})
        lat = location.get('latitude')
        lng = location.get('longitude')

        # Format the display name
        display_name = place_data.get('displayName', {})
        name = (
            display_name.get('text', '') 
            if isinstance(display_name, dict) else str(display_name)
        )

        # Extract address
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
        
