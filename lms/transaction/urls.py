from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TransactionViewSet,
    
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
router = DefaultRouter()
router.register(r'transaction', TransactionViewSet, basename='transaction')

urlpatterns = [
   

   
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('transaction/<int:barcode>/', TransactionViewSet.as_view({'get': 'retrieve'}), name='transaction-retrieve'),
    # Transaction-related endpoints
    path('', include(router.urls)),

    
]
