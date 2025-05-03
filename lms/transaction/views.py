from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .serializers import TransactionSerializer, TransactionResponse
from .services import TransactionService
from core.email import send_transaction_email
from core.utils import handle_error
import logging

logger = logging.getLogger(__name__)

#  Custom Pagination Class
class TransactionPagination(PageNumberPagination):
    page_size = 5  # Default page size
    page_size_query_param = "page_size"  # Allows client to set page size
    max_page_size = 50  # Prevents excessive load

class TransactionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    pagination_class = TransactionPagination  # Attach Pagination

    @handle_error
    def create(self, request):
        logger.info(f"Creating a new transaction with data: {request.data}")
        transaction_service = TransactionService()
        transaction_data = request.data
        ttype = transaction_data.get("transaction_type")

        if ttype == "Borrow":
            result = transaction_service.borrow_book(transaction_data)
            try:
                student_id = transaction_data.get("student", {}).get("student_id")
                send_transaction_email(student_id, result.transaction_id)
            except Exception as e:
                logger.error(f"Failed to send email: {e}")
        elif ttype == "Return":
            result = transaction_service.return_book(transaction_data)
            if isinstance(result, dict) and "error" in result:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Invalid transaction type"}, status=status.HTTP_400_BAD_REQUEST)

        if not result:
            return Response({"error": "Transaction failed"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TransactionSerializer(result)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @handle_error
    def retrieve(self, request, pk=None):
        logger.info(f"Fetching transaction with ID {pk}.")
        transaction_service = TransactionService()
        transaction = transaction_service.repo.get_transaction_by_id(pk)

        if not transaction:
            return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

    @handle_error
    def retrieve(self, request, barcode=None):
        logger.info(f"Fetching transaction with barcode {barcode}.")
        transaction_service = TransactionService()
        transaction = transaction_service.repo.get_transaction_by_barcode(barcode)

        if not transaction:
            return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TransactionResponse(transaction)
        return Response(serializer.data)

    @handle_error
    def update(self, request, pk=None):
        logger.info(f"Updating transaction with ID {pk} with data: {request.data}")
        transaction_service = TransactionService()
        student_id = request.data.get("student")
        result = transaction_service.return_book(student_id, pk)

        if not result or "error" in result:
            return Response({"error": "Failed to update transaction"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TransactionResponse(result)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @handle_error
    def list(self, request):
        logger.info("Fetching all transactions.")
        query = request.query_params.get("query", None)
        completed = request.query_params.get("completed", "false").lower() == "true"

        transaction_service = TransactionService()
        transactions = transaction_service.repo.get_all_transactions(query, completed)

        #  Apply Pagination
        paginator = self.pagination_class()
        paginated_transactions = paginator.paginate_queryset(transactions, request)

        serializer = TransactionResponse(paginated_transactions, many=True)
        return paginator.get_paginated_response(serializer.data)  # Returns paginated response

    @handle_error
    def destroy(self, request, pk=None):
        logger.info(f"Deleting transaction with ID {pk}.")
        transaction_service = TransactionService()
        result = transaction_service.repo.delete_transaction(pk)

        if not result:
            return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "Transaction deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    @handle_error
    def overdue(self, request):
        logger.info("Fetching overdue transactions.")
        transaction_service = TransactionService()
        overdue_transactions = transaction_service.update_book_status_on_due()

        #  Apply Pagination
        paginator = self.pagination_class()
        paginated_transactions = paginator.paginate_queryset(overdue_transactions, request)

        serializer = TransactionSerializer(paginated_transactions, many=True)
        return paginator.get_paginated_response(serializer.data)
