from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LoginView,
    RegisterUserView,
    UserView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
router = DefaultRouter()


urlpatterns = [
    # User-related endpoints
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('user/<str:username>/', UserView.as_view(), name='user'),

    # JWT token endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Employee-related endpoints
    path('', include(router.urls)),

    
]
