from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Expense, Category
from .forms import *
from django.contrib import messages

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


@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    return render(request, 'expense/expense_list.html', {
        'expenses': expenses
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
