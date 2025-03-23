from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
router = DefaultRouter()
router.register(r'author', AuthorViewSet, basename='author')

urlpatterns = [
   
    # Author-related endpoints
    path('', include(router.urls)),
    
]