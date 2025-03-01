from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date

# class Category(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name


class Expense(models.Model):
    CATEGORY = (
        ('', 'Select Category'),
        ('Clothing & Accessories', 'Clothing & Accessories'),
        ('Education', 'Education'),
        ('Entertainment', 'Entertainment'),
        ('Food', 'Food'),
        ('Health', 'Health'),
        ('Miscellaneous', 'Miscellaneous'),
        ('Others', 'Others'),
        ('Personal Care', 'Personal Care'),
        ('Transport', 'Transport'),
        ('Utilities', 'Utilities')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    category = models.CharField(max_length=200, choices=CATEGORY, default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    date = models.DateField()
        
    def clean(self):
        today = date.today()
        first_day = today.replace(day=1)

        if self.amount < 0:
            raise ValidationError("Amount cannot be negative.")

        if self.date < first_day or self.date > today:
            raise ValidationError("Date must be within the current month and not in the future.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user} - {self.amount} on {self.date}'



class Budget(models.Model):
    CATEGORY=(
        ('', 'Select Category'),
        ('Clothing & Accessories', 'Clothing & Accessories'),
        ('Education', 'Education'),
        ('Entertainment', 'Entertainment'),
        ('Food','Food'),
        ('Health', 'Health'),
        ('Miscellaneous', 'Miscellaneous'),
        ('Others', 'Others'),
        ('Personal Care', 'Personal Care'),
        ('Transport', 'Transport'),
        ('Utilities', 'Utilities')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, null=True)
    category = models.CharField(max_length=200, choices=CATEGORY, default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    rem_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    