import logging
import traceback

from django.utils import timezone
from django.contrib.auth.models import User

from apps.books.models import Book, Loan
from apps.books.serializers import LoanSerializer, BookSerializer


# Configure logging
logger = logging.getLogger(__name__)


class BookService:
    """
    Service for books.
    """

    def get_all_books(self):
        """
        Get all books.
        """
        return Book.objects.all()

    def get_book_by_id(self, book_id: int) -> Book:
        """
        Get a book by id.
        """
        return Book.objects.get(id=book_id)

    def create_book(self, title: str, author: str, isbn: str, page_count: int, description: str) -> Book:
        """
        Create a book.
        """
        return Book.objects.create(title=title, author=author, isbn=isbn, page_count=page_count, description=description)

    def check_book_availability(self, book_id: int) -> bool:
        """
        Check if a book is available.
        """
        return Book.objects.get(id=book_id).is_available

    def update_book_availability(self, book: Book, is_available: bool) -> dict:
        """
        Update a book's availability.
        """
        try:
            # Update book availability
            book.is_available = is_available
            book.save()
            
            return BookSerializer(book).data
        
        except Exception as e:
            logger.error(f"Internal server error: {e}")
            logger.error(traceback.format_exc())
            raise ValueError("Internal server error")


class LoanService:
    """
    Service for loans.
    """

    def __init__(self):
        self.book_service = BookService()

    def get_loan_by_id(self, loan_id: int) -> Loan:
        """
        Get a loan by id.
        """
        return Loan.objects.get(id=loan_id)

    def create_loan(self, book: Book, user: User) -> Loan:
        """
        Create a loan.
        """
        return Loan.objects.create(book=book, user=user, status='borrowed')
        
    def update_loan_status(self, loan: Loan, status: str) -> Loan:
        """
        Update a loan's status.
        """
        # Updating loan status
        loan.status = status
        if status == 'returned':
            loan.returned_at = timezone.now()
            loan.fine_amount = loan.calculate_fine()
        elif status == 'lost':
            loan.status = 'lost'
            loan.fine_amount = 100
        elif status == 'damaged':
            loan.status = 'damaged'
            loan.fine_amount = 50 
        else:
            raise ValueError("Invalid status")
        
        # Saving loan record
        loan.save()

        # Update book availability
        self.book_service.update_book_availability(loan.book, True)

        return loan


class BookBorrowService:
    """
    Service for borrowing a book.
    """

    def __init__(self):
        self.book_service = BookService()
        self.loan_service = LoanService()

    def borrow_book(self, book_id: int, user_id: int) -> dict:
        """
        Borrow a book for a user.
        """
        try:
            # Check if book is available or not
            if not self.book_service.check_book_availability(book_id):
                raise ValueError("Book is not available")

            # Fetch book and user
            book = self.book_service.get_book_by_id(book_id)
            user = User.objects.get(id=user_id)

            if not book or not user:
                raise ValueError("Book or user not found")
            
            # Create a loan record
            loan = self.loan_service.create_loan(book, user)

            # Update book availability
            self.book_service.update_book_availability(book, False)

            return LoanSerializer(loan).data
        
        except Exception as e:
            logger.error(f"Internal server error: {e}")
            logger.error(traceback.format_exc())
            raise ValueError("Internal server error")

    def return_book(self, loan_id: int) -> dict:
        """
        Return a book.
        """
        try:
            # Check if loan exists
            loan = self.loan_service.get_loan_by_id(loan_id)
            
            if not loan:
                raise ValueError("Loan not found")
            
            if loan.status != 'borrowed':
                raise ValueError("Loan is not borrowed")

            # Update loan status
            loan = self.loan_service.update_loan_status(loan, 'returned')
            return LoanSerializer(loan).data
        
        except Exception as e:
            logger.error(f"Internal server error: {e}")
            logger.error(traceback.format_exc())
            raise ValueError("Internal server error")