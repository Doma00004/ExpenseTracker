from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    date = models.DateField()

    def __str__(self):
        return f'{self.user} - {self.amount} on {self.date}'

class Budget(models.Model):
    PERIOD=(
        ('Week','Week'),
        ('Month', 'Month'),
        ('Year', 'Year')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    time_period = models.CharField(max_length=200, choices=PERIOD, default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    rem_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    