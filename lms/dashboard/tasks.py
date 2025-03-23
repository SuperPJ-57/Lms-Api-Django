from celery import shared_task
from .services import DashboardService
from .repositories import DashboardRepository

@shared_task
def send_overdue_emails():
    print("Task send_overdue_emails started")
    dashboard_service = DashboardService(DashboardRepository())
    overdue_borrowers = dashboard_service.email_get_overdue_borrowers()
    print(f"Task completed with {len(overdue_borrowers)} overdue borrowers")
    return {"message": "Emails sent to overdue borrowers", "count": len(overdue_borrowers)}