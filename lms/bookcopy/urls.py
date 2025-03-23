from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookCopyViewSet

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
router = DefaultRouter()
router.register(r'bookcopy', BookCopyViewSet, basename='bookcopy')

urlpatterns = [
   

   
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Book-related endpoints
    path('', include(router.urls)),

    
]
