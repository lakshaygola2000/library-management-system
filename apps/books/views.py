import logging
import traceback

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from apps.books.models import Book
from apps.books.permissions import IsAdminOrReadOnly
from apps.books.services import BookBorrowService, BookService
from apps.books.serializers import BookSerializer, LoanSerializer


# Configure logging
logger = logging.getLogger(__name__)


class BookListView(APIView):
    """
    View for listing all books.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = BookSerializer

    def get(self, request):
        try:
            
            # Get all books
            books = Book.objects.all()
            serializer = BookSerializer(books, many=True)
            
            return Response(data={
                "success": True,
                "message": "Books listed",
                "data": {
                    "books": serializer.data
                }
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Internal server error: {e}")
            logger.error(traceback.format_exc())
            return Response(data={
                "success": False,
                "message": "Internal server error",
                "data": {
                    "error": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddBookView(APIView):
    """
    View for adding a book.
    """
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)
    serializer_class = BookSerializer

    def post(self, request):
        try:
            # Fetch data from request
            serializer = self.serializer_class(data=request.data)

            # Validate data
            if serializer.is_valid():
                # Add book
                book = BookService().create_book(serializer.validated_data['title'], serializer.validated_data['author'], serializer.validated_data['isbn'], serializer.validated_data['page_count'], serializer.validated_data['description'])
                return Response(data={
                    "success": True,
                    "message": "Book added successfully",
                    "data": {
                        "book": BookSerializer(book).data
                    }
                }, status=status.HTTP_201_CREATED)
            else:
                return Response(data={
                    "success": False,
                    "message": "Validation errors",
                    "data": {
                        "errors": serializer.errors
                    }
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Internal server error: {e}")
            logger.error(traceback.format_exc())
            return Response(data={
                "success": False,
                "message": "Internal server error",
                "data": {
                    "error": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoanBookView(APIView):
    """
    View for borrowing a book.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = LoanSerializer

    def post(self, request):
        try:
            # Fetch data from request
            book_id = request.data.get('book_id')
            user_id = request.user.id

            # Borrow book
            loan = BookBorrowService().borrow_book(book_id, user_id)
            return Response(data={
                "success": True,
                "message": "Book borrowed successfully",
                "data": {
                    "loan": loan
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Internal server error: {e}")
            logger.error(traceback.format_exc())
            return Response(data={
                "success": False,
                "message": "Internal server error",
                "data": {
                    "error": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReturnBookView(APIView):
    """
    View for returning a book.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = LoanSerializer

    def post(self, request):
        try:
            # Fetch data from request
            loan_id = request.data.get('loan_id')
            user_id = request.user.id

            # Return book
            loan = BookBorrowService().return_book(loan_id)
            return Response(data={
                "success": True,
                "message": "Book returned successfully",
                "data": {
                    "loan": loan
                }
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Internal server error: {e}")
            logger.error(traceback.format_exc())
            return Response(data={
                "success": False,
                "message": "Internal server error",
                "data": {
                    "error": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)