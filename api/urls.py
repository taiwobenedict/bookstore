from django.urls import path
from .views import get_books, get_book_details, place_order, book_summary, get_order_status

urlpatterns = [
    path('books/', get_books),
    path('books/<int:book_id>/', get_book_details),
    path('orders/', place_order),
    path('orders/staus/', get_order_status ),
    path('book/summary/<int:book_id>/', book_summary ),
]
