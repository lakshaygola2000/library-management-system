from rest_framework import serializers

from django.contrib.auth.models import User

from apps.books.models import Book, Loan


class BookSerializer(serializers.ModelSerializer):
    is_available = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'available_copies')


class BookListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views"""
    is_available = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'genre', 'available_copies', 
                  'total_copies', 'is_available']


class LoanSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)
    
    class Meta:
        model = Loan
        fields = '__all__'
        read_only_fields = ('id', 'user', 'borrowed_at', 'status', 
                           'fine_amount', 'created_at', 'updated_at')


class BorrowBookSerializer(serializers.Serializer):
    book_id = serializers.UUIDField()
    
    def validate_book_id(self, value):
        try:
            book = Book.objects.get(id=value)
            if not book.is_available:
                raise serializers.ValidationError("This book is not available")
        except Book.DoesNotExist:
            raise serializers.ValidationError("Book not found")
        return value
