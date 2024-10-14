from django import forms
from .models import Expense, Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'description', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }
