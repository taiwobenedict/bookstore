from django.urls import path
from .views import *

urlpatterns = [
    path('', get_books, name="books"),
    path('books/<int:book_id>/', get_book_details, name="book"),
    path("dashboard", dashboard, name= "dashboard"),
    path("orders/status/", order_status, name= "order-status"),
    path('order/<int:book_id>/', place_order, name="order"),
    
    # Authentication
    path("register", register, name="register"),
    path("login", user_login, name="login"),
    path("logout", user_logout, name="logout")
]
