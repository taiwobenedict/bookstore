from django.shortcuts import render, redirect
from .models import Book, Order
from django.contrib.auth import login, logout, authenticate
from django.http import HttpRequest
from .forms import BookForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from services.ai import generate_book_summary


# Create your views here.



# Admin Dashbo
@login_required(login_url="login")
def dashboard(request: HttpRequest):
    
    form = BookForm()
    
    status = request.POST.get("status")
    order_id = request.POST.get("order_id")
    
    if status and order_id:
        order = Order.objects.get(id =order_id)
        order.status = status
        order.save()
        
        # Send WebSocket message to update order status in real-time
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "orders",
            {
                "type": "order_status_update",
                "order_id": order_id,
                "status": status,
            }
        )

        
    else:
        
    
        # Create New Book if it's a POST request
        if request.method == "POST":
            form = BookForm(request.POST)
            if form.is_valid():
                form.save()
                
                # Clear form after save
                form = BookForm()
        
    
    books = Book.objects.all()
    orders = Order.objects.all()
    context = {
        "form": form,
        'books': books,
        'orders': orders,
    }
    
    return render(request, "dashboard.html", context=context)


# Get All books
def get_books(request):
    books = Book.objects.all()
    context = {
        "books": books,
    }
    return render(request, "book_list.html", context)


# Get single book details
def get_book_details(request, book_id):
    book = Book.objects.get(id=book_id)
    stock = list(range(1, book.stock + 1))
    summary = generate_book_summary(book.title)

    context = {
 
        'book': book,
        'stock': stock,
        "summary": summary
    }
    return render(request, "book.html", context=context)


# Place order
@login_required(login_url="login")
def place_order(request: HttpRequest, book_id):
    
    
    if request.method == "GET":
        return redirect(f"/books/{book_id}/")
    
    qty = request.POST.get('qty')
    book = Book.objects.get(id=book_id)
 
    
    # Create Order for customer
    Order.objects.create(customer=request.user, book=book, quantity=int(qty))
    
    # Update Stock
    book.stock  = book.stock - int(qty)
    book.save()

    
    return redirect("order-status")


# Order Status
@login_required(login_url="login")
def order_status(request: HttpRequest):
    
    orders = Order.objects.filter(customer = request.user)
    context = {
        "orders":orders 
    }
    return render(request, "order_status.html", context=context)





# ======== AUTHENTICATION ==================

# Register Users
def register(request: HttpRequest):
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("username")
        
        user = User.objects.create_user(username=username, password= password)
    
        if user:
            login(request, user)
            next_url = request.GET.get("next") or request.POST.get("next") or "dashboard" if user.is_superuser else "books"  
            return redirect(next_url)
            

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
            next_url = request.GET.get("next") or request.POST.get("next") or "dashboard" if user.is_superuser else "books"  
            return redirect(next_url)
    
        else:
            context = {**context, "error": "Invalid Crendials"}


    return render(request, "auth.html", context=context)


# Logout Users
def user_logout(request):
    logout(request)
    return redirect("login")


# Documentation 
def documentation(request):
    
    return render(request, 'documentation.html')