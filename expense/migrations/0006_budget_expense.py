# Generated by Django 5.1.2 on 2024-10-14 11:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0005_budget_time_period'),
    ]

    operations = [
        migrations.AddField(
            model_name='budget',
            name='expense',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='expense.expense'),
        ),
    ]
