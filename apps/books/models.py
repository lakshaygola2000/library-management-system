from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Book(models.Model):
    """
    Model for a book.
    """

    id  = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13)
    page_count = models.IntegerField()
    is_available = models.BooleanField(default=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', 'is_available']
        indexes = [
            models.Index(fields=['is_available', 'title']),
            models.Index(fields=['isbn'])
        ]

    def __str__(self):
        return f"{self.title} by {self.author}"

    @property
    def borrow(self, user):
        """
        Borrow a book for a user.
        """
        if not self.is_available:
            raise ValueError("Book is not available")
        
        self.is_available = False
        self.borrowed_by = user
        self.borrowed_at = timezone.now()
        self.save()


class Loan(models.Model):
    """
    Model for a loan.
    """

    LOAN_STATUS_CHOICES = [
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('lost', 'Lost'),
        ('damaged', 'Damaged'),
    ]

    id = models.BigAutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, blank=True)
    fine_amount = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, choices=LOAN_STATUS_CHOICES, default='borrowed')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-borrowed_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['book', 'status'])
        ]

    def calculate_fine(self):
        """
        Calculate the fine amount for the loan.
        """
        if self.status == 'borrowed':
            return 0
        elif self.status == 'returned':
            return 0
        elif self.status == 'lost':
            return 100
        elif self.status == 'damaged':
            return 50
        else:
            return 0

    def __str__(self):
        return f"{self.book.title} borrowed by {self.user.username}"
