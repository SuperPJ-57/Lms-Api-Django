from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from .serializers import TransactionSerializer, TransactionResponse
from .services import TransactionService
from core.email import send_transaction_email
from core.utils import handle_error
import logging
logger = logging.getLogger(__name__)


class TransactionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @handle_error
    def create(self, request):
        logger.info(f"Creating a new transaction with data: {request.data}")
        transaction_service = TransactionService()
        transaction_data = request.data
        ttype = transaction_data.get('transaction_type')

        if ttype == 'Borrow':
            result = transaction_service.borrow_book(transaction_data)
            try:
                # userId = transaction_data.user.userId
                student_id = transaction_data['student'].student_id
                send_transaction_email(student_id, result.transaction_id)
            except Exception as e:
                logger.error(f"Failed to send email: {e}")
        elif ttype == 'Return':
            
            result = transaction_service.return_book(transaction_data)
            
            if isinstance(result,dict) and 'error' in result:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Invalid transaction type"}, status=status.HTTP_400_BAD_REQUEST)
        
        if result is None:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = TransactionSerializer(result)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    @handle_error
    def retrieve(self, request, pk=None):
        logger.info(f"Fetching transaction with id {pk}.")
        transaction_service = TransactionService()
        transaction = transaction_service.repo.get_transaction_by_id(pk)
        
        if not transaction:
            return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)


    @handle_error
    def update(self, request, pk=None):
        logger.info(f"Updating transaction with id {pk} with data: {request.data}")
        transaction_service = TransactionService()
        student_id = request.data.get('student')
        result = transaction_service.return_book(student_id, pk)
        
        if result is None or "error" in result:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = TransactionSerializer(result)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @handle_error
    def list(self, request):
        logger.info("Fetching all transactions.")
        transaction_service = TransactionService()
        transactions = transaction_service.repo.get_all_transactions()
        
        serializer = TransactionResponse(transactions, many=True)
        return Response(serializer.data)


    @handle_error
    def destroy(self, request, pk=None):
        logger.info(f"Deleting transaction with id {pk}.")
        transaction_service = TransactionService()
        result = transaction_service.repo.delete_transaction(pk)
        
        if not result:
            return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({"message": "Transaction deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


    @handle_error
    def overdue(self, request):
        transaction_service = TransactionService()
        overdue_transactions = transaction_service.update_book_status_on_due()
        
        serializer = TransactionSerializer(overdue_transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)