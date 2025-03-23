from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from celery import shared_task
from .serializers import DashboardSerializer, OverdueBorrowerSerializer
from .tasks import send_overdue_emails
from .models import OverdueBorrower
from .services import DashboardService
from celery.result import AsyncResult
from rest_framework.views import APIView


class DashboardViewSet(viewsets.ViewSet):
    #permission_classes = [IsAuthenticated]

    def retrieve(self, request, username=None):
        # service = DashboardService()
        dashboard_data = DashboardService.get_dashboard_data(username)
        serializer = DashboardSerializer(dashboard_data)
        return Response(serializer.data)
        
class GetOverdueBorrowersViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def retrieve(self, request):
        service = DashboardService()
        overdue_borrowers = service.get_overdue_borrowers()  # Emails are sent here
        serializer = OverdueBorrowerSerializer(overdue_borrowers, many=True)
        return Response(serializer.data)
    
class MailOverdueBorrowersView(viewsets.ViewSet):
    """
    Sends emails to overdue borrowers asynchronously using Celery and returns a confirmation message.
    """
    permission_classes = [IsAuthenticated]

    def retrieve(self, request):
        # Call the Celery task to send emails asynchronously
        task_result = send_overdue_emails.delay()  # Use .delay() to run the task asynchronously
        
        # Return a response with the task ID for tracking
        return Response({
            "message": "Emails are being sent to overdue borrowers asynchronously.",
            "task_id": task_result.id  # Include the task ID for tracking
        })
    


class TaskStatusView(APIView):
    """
    Check the status of a Celery task.
    """
    def get(self, request, task_id):
        task_result = AsyncResult(task_id)
        return Response({
            "task_id": task_id,
            "status": task_result.status,
            "result": task_result.result
        })