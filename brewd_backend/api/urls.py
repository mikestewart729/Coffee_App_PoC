# urls.py
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    signup, current_user, update_user_location
)

urlpatterns = [
    # Registration
    path('signup/', signup, name='signup'),
    # Authentication
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/user/', current_user, name='current_user'),
    # User location update
    path('user/update_location/', update_user_location, name='update_user_location'),
]