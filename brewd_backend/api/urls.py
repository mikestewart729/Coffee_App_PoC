# urls.py
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    signup, current_user
)

urlpatterns = [
    # Registration
    path('signup/', signup, name='signup'),
    # Authentication
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/user/', current_user, name='current_user'),
]