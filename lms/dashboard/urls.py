from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DashboardViewSet,
    GetOverdueBorrowersViewSet,
    MailOverdueBorrowersView,
    TaskStatusView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

urlpatterns = [
    path('overdue-borrowers/', GetOverdueBorrowersViewSet.as_view({'get': 'retrieve'}), name='overdue-borrowers-retrieve'),
    path('mail-overdue-borrowers/', MailOverdueBorrowersView.as_view({'get': 'retrieve'}), name='mail-overdue-borrowers'),
    path('dashboard/<str:username>/', DashboardViewSet.as_view({'get': 'retrieve'}), name='dashboard-retrieve'),
    path('task-status/<str:task_id>/', TaskStatusView.as_view(), name='task-status'),
    path('', include(router.urls)),
]