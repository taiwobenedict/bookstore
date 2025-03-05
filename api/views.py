from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from product.models import Book, Order
from product.serializers import BookSerializer, OrderSerializer
from services.ai import generate_book_summary
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

# Create your views here.

# GET ALL BOOKS
@api_view(['GET'])
def get_books(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

# GET SINGLE BOOK 
@api_view(['GET'])
def get_book_details(request, book_id):
    book = Book.objects.get(id=book_id)
    serializer = BookSerializer(book)
    return Response(serializer.data)


# PLACE ODER
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_order(request):
    print(request.user.id)
    request.data['customer'] = request.user.id
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        order = serializer.save()
        # Publish message to NATS
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

# {"book":2, "quantity":1}
# GET ORDER STATUS
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_status(request):
    order = Order.objects.filter(customer = request.user)
    serializer = OrderSerializer(order, many=True)
    return Response(serializer.data)


# GET BOOK SUMMARY
@api_view(['GET'])
def book_summary(request, book_id):
    
    book = Book.objects.get(id = book_id)
    summary = generate_book_summary(book_title=book.title)
    return Response({"data": summary}, status=status.HTTP_200_OK)




