from django import forms
from .models import *
from datetime import date

# class CategoryForm(forms.ModelForm):
#     class Meta:
#         model = Category
#         fields = ['name']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['name', 'category', 'amount', 'description', 'date']
        widgets = {
            'amount': forms.NumberInput(attrs={'min': '1'}),
            'date': forms.DateInput(attrs={'type': 'date', 'id': 'expense_date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = date.today()
        first_day = today.replace(day=1)
        self.fields['date'].widget.attrs['max'] = today.strftime('%Y-%m-%d')
        self.fields['date'].widget.attrs['min'] = first_day.strftime('%Y-%m-%d')

    def clean_amount(self):
            amount = self.cleaned_data.get('amount')
            if amount < 1:
                raise forms.ValidationError("Amount cannot be negative.")
            return amount
    


# class ExpenseForm(forms.ModelForm):
#     class Meta:
#         model = Expense
#         fields = ['name', 'category', 'amount', 'description', 'date']
#         widgets = {
#             'date': forms.DateInput(attrs={'type': 'date'})
#         }

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'min': '1'})
        }

    def clean_amount(self):
            amount = self.cleaned_data.get('amount')
            if amount < 1:
                raise forms.ValidationError("Amount cannot be negative.")
            return amount