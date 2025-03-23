from .repositories import DashboardRepository
from core.email import send_email


class DashboardService:
    def __init__(self):
        self.repository = DashboardRepository()

    @staticmethod
    def get_dashboard_data(username):
        

        borrowed_books_count = DashboardRepository.get_borrowed_books_count()
        total_books = DashboardRepository.get_total_books()
        returned_books_count = DashboardRepository.get_returned_books_count()
        total_students = DashboardRepository.get_total_students()
        available_books_count = DashboardRepository.get_available_books_count()
        total_faculty = DashboardRepository.get_total_faculty()
        user = DashboardRepository.get_user(username)
        total_transaction_count = DashboardRepository.get_total_transactions()


        return {
            'total_borrowed_books': borrowed_books_count,
            'total_books': total_books,
            'total_returned_books': returned_books_count,
            'total_user_base': total_students,
            'available_books': available_books_count,
            'total_faculty': total_faculty,
            'user': user,
            'total_transaction_count': total_transaction_count,
            
            # 'overdue_borrowers': list(repo.get_overdue_borrowers().values())
            
        }
    
    
    
    def get_overdue_borrowers(self):
        overdue_borrowers = DashboardRepository.get_overdue_borrowers()
        return overdue_borrowers
    
    def email_get_overdue_borrowers(self):
        overdue_borrowers = DashboardRepository.get_overdue_borrowers()

        for borrower in overdue_borrowers:
            subject = "Library Overdue Notice"
            message = (
                f"Dear {borrower.student.name},\n\n"
                "Our records show that you have an overdue book borrowed from the library. "
                "Please return it as soon as possible to avoid penalties.\n\n"
                "Thank you."
            )
            recipient_email = borrower.student.email

            # Use EmailHelper
            send_email(subject, message, recipient_email)

        return overdue_borrowers