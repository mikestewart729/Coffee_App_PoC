from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser
    """
    location_lat = models.FloatField(null=True, blank=True)
    location_lng = models.FloatField(null=True, blank=True)
    default_search_radius = models.IntegerField(default=1610)  # meters, ~1 mile
    
    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return self.username
