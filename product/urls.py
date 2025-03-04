from django.urls import path
from .views import *

urlpatterns = [
    path('', get_books),
    path('books/<int:book_id>/', get_book_details, name="book_details"),
    path('orders/', place_order),
    path("dashboard", dashboard, name= "dashboard"),
    path("orders/status/", order_status, name= "order-status"),
    
    path("login", user_login, name="login"),
    path("logout", user_logout, name="logout")
]
