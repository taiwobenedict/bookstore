from rest_framework import serializers
from .models import Book, Order

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'book', 'quantity', 'status', 'total_price']  # Include total_price

    def get_total_price(self, obj):
        return obj.total_price  # Calls the @property method in the model