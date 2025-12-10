from django.urls import path

from apps.books.views import (
    BookListView,
    AddBookView,
    LoanBookView,
    ReturnBookView,
)

urlpatterns = [
    path('list/', BookListView.as_view(), name='book-list'),
    path('add/', AddBookView.as_view(), name='add-book'),
    path('loan/', LoanBookView.as_view(), name='loan-book'),
    path('return/', ReturnBookView.as_view(), name='return-book'),
]