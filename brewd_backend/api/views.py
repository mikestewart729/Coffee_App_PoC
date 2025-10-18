from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import User
from .serializers import UserSerializer

# ============ Authentication Views ============
@api_view(['GET'])
def current_user(request):
    """Get current authenticated user"""
    serializer = UserSerializer(request.user)
    return JsonResponse(serializer.data)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data

    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        try:
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data.get('email', ''),
                password=request.data['password']
            )
            return JsonResponse({
                'success': True,
                'user': UserSerializer(user).data
            }, status=201)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    else:
        return JsonResponse({
            'success': False,
            'errors': serializer.errors
        }, status=400)
