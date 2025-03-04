from django.shortcuts import render, redirect
from .models import Book, Order
from django.contrib.auth import login, logout, authenticate
from django.http import HttpRequest
from .forms import BookForm

# Create your views here.



# Admin Dashbo
def dashboard(request: HttpRequest):
    
    
    
    form = BookForm()
    
    # Create New Book if it's a POST request
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
    
    
    books = Book.objects.all()
    context = {
        "form": form,
        'books': books
    }
    
    return render(request, "dashboard.html", context=context)


def get_books(request):
    books = Book.objects.all()
    context = {
        "books": books,
    }
    return render(request, "book_list.html", context)


def get_book_details(request, book_id):
    book = Book.objects.get(id=book_id)
    return render(request, "book.html")


def place_order(request: HttpRequest):
    return render(request, "order_status.html")


def order_status(request: HttpRequest):
    return render(request, "order_status.html")


# ======== AUTHENTICATION ==================

# Register Users
def register_user(request: HttpRequest):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("username")

    context = {"page": "register"}

    return render(request, "auth.html", context=context)


# Login Users
def user_login(request: HttpRequest):
    context = {"page": "login"}

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username)
        print(password)

        user = authenticate(request, username=username, password=password)
        print(user)
        if user:
            login(request, user)
            if request.user.is_superuser:
                return redirect("dashboard")
            else:
                return redirect("order-staus")
        else:
            context = {**context, "error": "Invalid Crendials"}


    return render(request, "auth.html", context=context)


# Logout Users
def user_logout(request):
    logout(request)
    return redirect("login")
