from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    
    class Meta:
        model = Book
        fields = "__all__"
        widgets = {
            "title": forms.TextInput(attrs={'class': 'form-control'}),
            "author": forms.TextInput(attrs={'class': 'form-control'}),
            "description": forms.TextInput(attrs={'class': 'form-control'}),
            "price": forms.NumberInput(attrs={'class': 'form-control'}),
            "stock": forms.NumberInput(attrs={'class': 'form-control'}),
        }
