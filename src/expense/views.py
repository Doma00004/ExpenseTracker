from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Expense, Category
from .forms import *
from django.contrib import messages
from django.db.models import Sum
from collections import defaultdict
from datetime import datetime, timedelta
from django.utils.timezone import now

# category section start

@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'expense/category_list.html', {
        'categories': categories
    })

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.add_message(request, messages.SUCCESS, "Category added successfully !")
            return redirect('category_list')
        else:
            messages.add_message(request, messages.ERROR, 'Please verify form')
            form = CategoryForm()
            return render(request, 'expense/add_category.html', {
                'form': form
            })
    return render(request, 'expense/add_category.html', {
        'form': CategoryForm
    })

@login_required
def update_category(request, category_id):
    instance = Category.objects.get(id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=instance)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.add_message(request,messages.SUCCESS, 'Category updated')
            return redirect('category_list')
        else:
            messages.add_message(request, messages.ERROR, 'Please verify form')
            return render(request, 'expense/update_category.html', {
                'form':form
            })
    context = {
        'form':CategoryForm(instance=instance)
    }

    return render(request, 'expense/update_category.html', context)

@login_required
def delete_category(request, category_id):
    category = Category.objects.get(id = category_id)
    category.delete()
    messages.add_message(request, messages.SUCCESS,'Category deleted')
    return redirect('category_list')

# category section end



# expense section start

@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    
    # Group by date
    grouped_expenses = defaultdict(list)
    for expense in expenses:
        grouped_expenses[expense.date].append(expense)

    # Calculate totals
    expenses_with_totals = [
        {
            "date": date,
            "expenses": grouped_expenses[date],
            "total": sum(exp.amount for exp in grouped_expenses[date])
        }
        for date in sorted(grouped_expenses.keys(), reverse=True)
    ]

    return render(request, 'expense/expense_list.html', {
        'expenses_with_totals': expenses_with_totals
    })


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.add_message(request, messages.SUCCESS, "Expense added successfully !")
            return redirect('expense_list')
        else:
            messages.add_message(request, messages.ERROR, 'Please verify form')
            form = ExpenseForm()
            return render(request, 'expense/add_expense.html', {
                'form': form
            })
    return render(request, 'expense/add_expense.html', {
        'form': ExpenseForm
    })

@login_required
def update_expense(request, expense_id):
    instance = Expense.objects.get(id=expense_id)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS, 'Expense updated')
            return redirect('expense_list')
        else:
            messages.add_message(request, messages.ERROR, 'Please verify form')
            return render(request, 'expense/update_expense.html', {
                'form':form
            })
    context = {
        'form':ExpenseForm(instance=instance)
    }

    return render(request, 'expense/update_expense.html', context)

@login_required
def delete_expense(request, expense_id):
    expense = Expense.objects.get(id = expense_id)
    expense.delete()
    messages.add_message(request, messages.SUCCESS,'Expense deleted')
    return redirect('expense_list')

# expense section end


# budget section start

@login_required
def budget_list(request):
    budgets = Budget.objects.all()
    return render(request, 'expense/budget_list.html', {
        'budgets': budgets
    })

@login_required
def add_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            messages.add_message(request, messages.SUCCESS, "Budget added successfully !")
            return redirect('budget_list')
        else:
            messages.add_message(request, messages.ERROR, 'Please verify form')
            form = BudgetForm()
            return render(request, 'expense/add_budget.html', {
                'form': form
            })
    return render(request, 'expense/add_budget.html', {
        'form': BudgetForm
    })

@login_required
def update_budget(request, budget_id):
    instance = Budget.objects.get(id=budget_id)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=instance)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            messages.add_message(request,messages.SUCCESS, 'Budget updated')
            return redirect('budget_list')
        else:
            messages.add_message(request, messages.ERROR, 'Please verify form')
            return render(request, 'expense/update_budget.html', {
                'form':form
            })
    context = {
        'form':BudgetForm(instance=instance)
    }
    return render(request, 'expense/update_budget.html', context)

@login_required
def delete_budget(request, budget_id):
    budget = Budget.objects.get(id = budget_id)
    budget.delete()
    messages.add_message(request, messages.SUCCESS,'Budget deleted')
    return redirect('budget_list')

# budget section end


# @login_required
# def lhomepage(request):
#     budgets = Budget.objects.filter(user=request.user)
#     weekly_budgets = [
#         {
#             'category': budget.category,
#             'weekly_budget': budget.amount / (52 if budget.time_period == 'year' else (4 if budget.time_period == 'month' else 1)),
#             'original_amount': budget.amount,
#             'duration': budget.time_period,
#         }
#         for budget in budgets
#     ]

#     # Calculate total budget
#     total_budget = budgets.aggregate(Sum('amount'))['amount__sum'] or 0

#     # Calculate expenses for each category
#     category_data = []
#     for category in budgets.values_list('category', flat=True).distinct():
#         expenses = Expense.objects.filter(user=request.user, category=category).aggregate(Sum('amount'))['amount__sum'] or 0
#         budget_amount = budgets.filter(category=category).aggregate(Sum('amount'))['amount__sum'] or 0
#         remaining = budget_amount - expenses

#         category_data.append({
#             'category': category,
#             'budget': budget_amount,
#             'expenses': expenses,
#             'remaining': remaining
#         })

#     return render(request, 'expense/lhomepage.html', {
#         'weekly_budgets': weekly_budgets,
#         'total_budget': total_budget,
#         'category_data': category_data,
#     })

from django.db.models import Sum, F, Func
from django.db.models.functions import ExtractWeek, ExtractYear
from datetime import timedelta, date

@login_required
def budget_view(request):
    categories = Budget.objects.filter(user=request.user).values_list('category', flat=True).distinct()
    selected_category = request.GET.get('category', categories[0] if categories else None)

    weekly_budget = None
    weekly_expenses = []
    remaining_budget = 0
    total_expenses = 0

    if selected_category:
        # Get the budget for the selected category
        budget = Budget.objects.filter(user=request.user, category=selected_category).first()
        weekly_budget = (
            budget.amount / 52 if budget.time_period == 'year'
            else budget.amount / 4 if budget.time_period == 'month'
            else budget.amount
        )

        # Get weekly expenses for the selected category
        start_of_week = date.today() - timedelta(days=date.today().weekday())  # This week's Sunday
        end_of_week = start_of_week + timedelta(days=6)  # This week's Saturday

        weekly_expenses = (
            Expense.objects.filter(
                user=request.user,
                category=selected_category,
                date__range=[start_of_week, end_of_week]
            )
            .values('name', 'description', 'amount', 'date')
        )

        total_expenses = sum(expense['amount'] for expense in weekly_expenses)
        remaining_budget = weekly_budget - total_expenses if weekly_budget else 0

    return render(request, 'expense/budget_view.html', {
        'categories': categories,
        'selected_category': selected_category,
        'weekly_budget': weekly_budget,
        'weekly_expenses': weekly_expenses,
        'total_expenses': total_expenses,
        'remaining_budget': remaining_budget,
    })


# @login_required
# def lhomepage(request):
#     categories = Category.objects.filter()
#     expenses = Expense.objects.filter(user=request.user).order_by('-date')
#     budgets = Budget.objects.filter(user=request.user)

#     grouped_expenses = defaultdict(list)
#     for expense in expenses:
#         grouped_expenses[expense.date].append(expense)

#     # Calculate totals
#     expenses_with_totals = [
#         {
#             "date": date,
#             "expenses": grouped_expenses[date],
#             "total": sum(exp.amount for exp in grouped_expenses[date])
#         }
#         for date in sorted(grouped_expenses.keys(), reverse=True)
#     ]

#     weekly_budgets = [
#         {
#             'category': budget.category,
#             'weekly_budget': budget.amount / (52 if budget.time_period == 'year' else (4 if budget.time_period == 'month' else 1)),
#             'original_amount': budget.amount,
#             'duration': budget.time_period,
#         }
#         for budget in budgets
#     ]

#     # Calculate total budget
#     total_budget = budgets.aggregate(Sum('amount'))['amount__sum'] or 0

#     # Calculate expenses for each category
#     category_data = []
#     for category in budgets.values_list('category', flat=True).distinct():
#         expenses = Expense.objects.filter(user=request.user, category=category).aggregate(Sum('amount'))['amount__sum'] or 0
#         budget_amount = budgets.filter(category=category).aggregate(Sum('amount'))['amount__sum'] or 0
#         remaining = budget_amount - expenses

#         category_data.append({
#             'category': category,
#             'budget': budget_amount,
#             'expenses': expenses,
#             'remaining': remaining
#         })

#     return render(request, 'expense/lhomepage.html', {
#         'weekly_budgets': weekly_budgets,
#         'total_budget': total_budget,
#         'category_data': category_data,
#         'categories': categories,
#         'expenses_with_totals': expenses_with_totals,
#     })



@login_required
def report(request):
    categories = Category.objects.filter()
    selected_category = request.GET.get('category')  # Get selected category

    # Filter expenses by user and optionally by category
    expenses = Expense.objects.filter(user=request.user)
    if selected_category:
        expenses = expenses.filter(category__name=selected_category)
    
    # Filter by current week
    today = now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Start of the week (Monday)
    expenses = expenses.filter(date__gte=start_of_week)

    # Group expenses by date
    grouped_expenses = defaultdict(list)
    for expense in expenses:
        grouped_expenses[expense.date].append(expense)

    # Calculate totals for displayed expenses
    expenses_with_totals = [
        {
            "date": date,
            "expenses": grouped_expenses[date],
            "total": sum(exp.amount for exp in grouped_expenses[date]),
        }
        for date in sorted(grouped_expenses.keys(), reverse=True)
    ]

    # Get budgets and calculate totals for the selected category
    budgets = Budget.objects.filter(user=request.user)
    if selected_category:
        budgets = budgets.filter(category__name=selected_category)

    weekly_budget = [
    {
        'weekly_budget': round(
            budget.amount / 52 
            if budget.time_period.lower() == 'year' 
            else (budget.amount / 4 if budget.time_period.lower() == 'month' 
                  else budget.amount), 2  # Default is weekly
        ),
    }
    for budget in budgets
    ]

    total_budget = sum(budget['weekly_budget'] for budget in weekly_budget)
    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    remaining_budget = total_budget - total_expenses

    return render(request, 'expense/report.html', {
        'categories': categories,
        'expenses_with_totals': expenses_with_totals,
        'total_budget': total_budget,
        'total_expenses': total_expenses,
        'remaining_budget': remaining_budget,
        'selected_category': selected_category,
    })

