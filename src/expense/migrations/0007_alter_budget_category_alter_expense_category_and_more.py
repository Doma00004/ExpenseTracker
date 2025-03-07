# Generated by Django 5.1.2 on 2025-02-13 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0006_budget_expense'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='category',
            field=models.CharField(choices=[('Clothing & Accessories', 'Clothing & Accessories'), ('Education', 'Education'), ('Entertainment', 'Entertainment'), ('Food', 'Food'), ('Health', 'Health'), ('Miscellaneous', 'Miscellaneous'), ('Others', 'Others'), ('Personal Care', 'Personal Care'), ('Transport', 'Transport'), ('Utilities', 'Utilities')], default=1, max_length=200),
        ),
        migrations.AlterField(
            model_name='expense',
            name='category',
            field=models.CharField(choices=[('Clothing & Accessories', 'Clothing & Accessories'), ('Education', 'Education'), ('Entertainment', 'Entertainment'), ('Food', 'Food'), ('Health', 'Health'), ('Miscellaneous', 'Miscellaneous'), ('Others', 'Others'), ('Personal Care', 'Personal Care'), ('Transport', 'Transport'), ('Utilities', 'Utilities')], default=1, max_length=200),
        ),
        migrations.RemoveField(
            model_name='budget',
            name='time_period',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
