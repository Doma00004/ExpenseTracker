from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Expense
from .forms import *
from django.contrib import messages
from django.db.models import Sum
from collections import defaultdict
from datetime import datetime, timedelta
from django.utils.timezone import now

# category section start

# @login_required
# def category_list(request):
#     categories = Category.objects.all()
#     return render(request, 'expense/category_list.html', {
#         'categories': categories
#     })

# @login_required
# def add_category(request):
#     if request.method == 'POST':
#         form = CategoryForm(request.POST)
#         if form.is_valid():
#             category = form.save(commit=False)
#             category.user = request.user
#             category.save()
#             messages.add_message(request, messages.SUCCESS, "Category added successfully !")
#             return redirect('category_list')
#         else:
#             messages.add_message(request, messages.ERROR, 'Please verify form')
#             form = CategoryForm()
#             return render(request, 'expense/add_category.html', {
#                 'form': form
#             })
#     return render(request, 'expense/add_category.html', {
#         'form': CategoryForm
#     })

# @login_required
# def update_category(request, category_id):
#     instance = Category.objects.get(id=category_id)
#     if request.method == 'POST':
#         form = CategoryForm(request.POST, instance=instance)
#         if form.is_valid():
#             category = form.save(commit=False)
#             category.user = request.user
#             category.save()
#             messages.add_message(request,messages.SUCCESS, 'Category updated')
#             return redirect('category_list')
#         else:
#             messages.add_message(request, messages.ERROR, 'Please verify form')
#             return render(request, 'expense/update_category.html', {
#                 'form':form
#             })
#     context = {
#         'form':CategoryForm(instance=instance)
#     }

#     return render(request, 'expense/update_category.html', context)

# @login_required
# def delete_category(request, category_id):
#     category = Category.objects.get(id = category_id)
#     category.delete()
#     messages.add_message(request, messages.SUCCESS,'Category deleted')
#     return redirect('category_list')

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
            category = expense.category
            amount = expense.amount

            # Check if a budget is allocated for this category
            budget = Budget.objects.filter(user=request.user, category=category).first()
            
            if not budget:
                messages.error(request, 'No budget is allocated for this category.')
                return render(request, 'expense/add_expense.html', {'form': form})
            
            # Get current year and month
            current_year = now().year
            current_month = now().month

            # Calculate total expenses for this category in the current month
            total_expenses = Expense.objects.filter(
                user=request.user,
                category=category,
                date__year=current_year,
                date__month=current_month
            ).aggregate(total=Sum('amount'))['total'] or 0
            remaining_budget = budget.amount - total_expenses

            print(f"Budget Amount: {budget.amount}")  # Debugging line
            print(f"Total Expenses: {total_expenses}")  # Debugging line
            print(f"Remaining Budget: {remaining_budget}")

            if amount > remaining_budget:
                messages.error(request, f'Expense exceeds budget. Available Budget: Rs. {remaining_budget}')
                return render(request, 'expense/add_expense.html', {'form': form})

            # Save expense if all conditions are met

            expense.save()
            messages.add_message(request, messages.SUCCESS, "Expense added successfully !")
            return redirect('add_expense')
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
            return redirect('add_expense')
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
    budgets = Budget.objects.filter(user=request.user)
    return render(request, 'expense/budget_list.html', {
        'budgets': budgets
    })

@login_required
def add_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            amount = form.cleaned_data['amount']
            
            # Check if a budget already exists for this user and category
            budget = Budget.objects.filter(user=request.user, category=category).first()

            if budget:
                # If budget exists, update the amount
                budget.amount += amount
                budget.save()
                messages.success(request, f'Budget updated! New budget for {category}: Rs. {budget.amount:.2f}')
            else:
                # If no budget exists, create a new one
                new_budget = form.save(commit=False)
                new_budget.user = request.user
                new_budget.save()
                messages.success(request, "Budget added successfully!")

            return redirect('add_budget')

        else:
            messages.error(request, 'Please verify the form.')

    else:
        form = BudgetForm()

    return render(request, 'expense/add_budget.html', {'form': form})

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
            return redirect('add_budget')
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


# report section start

# @login_required
# def report(request):
#     categories = Category.objects.filter()
#     selected_category = request.GET.get('category')  # Get selected category

#     # Filter expenses by user and optionally by category
#     expenses = Expense.objects.filter(user=request.user)
#     if selected_category:
#         expenses = expenses.filter(category__name=selected_category)
    
#     # Filter by current week
#     today = now().date()
#     start_of_week = today - timedelta(days=today.weekday())  # Start of the week (Monday)
#     expenses = expenses.filter(date__gte=start_of_week)

#     # Group expenses by date
#     grouped_expenses = defaultdict(list)
#     for expense in expenses:
#         grouped_expenses[expense.date].append(expense)

#     # Calculate totals for displayed expenses
#     expenses_with_totals = [
#         {
#             "date": date,
#             "expenses": grouped_expenses[date],
#             "total": sum(exp.amount for exp in grouped_expenses[date]),
#         }
#         for date in sorted(grouped_expenses.keys(), reverse=True)
#     ]

#     # Get budgets and calculate totals for the selected category
#     budgets = Budget.objects.filter(user=request.user)
#     if selected_category:
#         budgets = budgets.filter(category__name=selected_category)

#     weekly_budget = [
#     {
#         'weekly_budget': round(
#             budget.amount / 52 
#             if budget.time_period.lower() == 'year' 
#             else (budget.amount / 4 if budget.time_period.lower() == 'month' 
#                   else budget.amount), 2  # Default is weekly
#         ),
#     }
#     for budget in budgets
#     ]

#     total_budget = sum(budget['weekly_budget'] for budget in weekly_budget)
#     total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
#     remaining_budget = total_budget - total_expenses

#     return render(request, 'expense/report.html', {
#         'categories': categories,
#         'expenses_with_totals': expenses_with_totals,
#         'total_budget': total_budget,
#         'total_expenses': total_expenses,
#         'remaining_budget': remaining_budget,
#         'selected_category': selected_category,
#     })

# report section end



# @login_required
# def report(request):
#     category = request.GET.get('category', '')  # Get category from URL query params

#     # Fetch expenses based on category
#     if category:
#         expenses = Expense.objects.filter(user=request.user, category=category)
#         total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
#         total_budget = Budget.objects.filter(user=request.user, category=category).aggregate(Sum('amount'))['amount__sum'] or 0
#     else:
#         expenses = Expense.objects.filter(user=request.user)
#         total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
#         total_budget = Budget.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0

#     remaining_budget = total_budget - total_expense

#     context = {
#         'expenses': expenses,
#         'categories': Expense.CATEGORY,
#         'selected_category': category,
#         'total_expense': total_expense,
#         'total_budget': total_budget,
#         'remaining_budget': remaining_budget
#     }

#     return render(request, 'expense_report.html', context)



@login_required
def report(request):
    categories = Expense.CATEGORY  # Fetch categories from the model
    selected_category = request.GET.get('category', '')  # Get selected category from query params

    # Get current month range
    today = now().date()
    start_of_month = today.replace(day=1)  # First day of the current month

    # Filter expenses by user and current month
    expenses = Expense.objects.filter(user=request.user, date__gte=start_of_month)
    
    if selected_category:
        expenses = expenses.filter(category=selected_category)

    # Group expenses by date
    grouped_expenses = defaultdict(list)
    for expense in expenses:
        grouped_expenses[expense.date].append(expense)

    # Create a list with totals
    expenses_with_totals = [
        {
            "date": date,
            "expenses": grouped_expenses[date],
            "total": sum(exp.amount for exp in grouped_expenses[date]),
        }
        for date in sorted(grouped_expenses.keys(), reverse=True)
    ]

    # Filter budgets by user and category
    budgets = Budget.objects.filter(user=request.user)
    
    if selected_category:
        budgets = budgets.filter(category=selected_category)

    
    # else:
    #     total_budget = budgets.aggregate(Sum('amount'))['amount__sum']
    #     remaining_budget = total_budget - total_expenses

    # Calculate total budget
    total_budget = budgets.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    remaining_budget = total_budget - total_expenses

    if not budgets.exists():
        total_budget = 0
        remaining_budget = 0

    return render(request, 'expense/mreport.html', {
        'categories': categories,
        'expenses_with_totals': expenses_with_totals,
        'total_budget': total_budget,
        'total_expenses': total_expenses,
        'remaining_budget': remaining_budget,
        'selected_category': selected_category,
    })



# import json
# from collections import defaultdict
# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from django.utils.timezone import now
# from django.db.models import Sum
# from .models import Expense, Budget  

# @login_required
# def report(request):
#     categories = Expense.CATEGORY  # Fetch categories from the model
#     selected_category = request.GET.get('category', '')

#     today = now().date()
#     start_of_month = today.replace(day=1)

#     expenses = Expense.objects.filter(user=request.user, date__gte=start_of_month)

#     if selected_category:
#         expenses = expenses.filter(category=selected_category)

#     # Aggregate expenses per category and convert to float
#     category_expense_data = expenses.values('category').annotate(total=Sum('amount'))

#     labels = [entry['category'] for entry in category_expense_data]
#     data = [float(entry['total']) for entry in category_expense_data]  # Convert Decimal to float

#     # Budget calculations
#     budgets = Budget.objects.filter(user=request.user)
#     if selected_category:
#         budgets = budgets.filter(category=selected_category)

#     total_budget = float(budgets.aggregate(Sum('amount'))['amount__sum'] or 0)
#     total_expenses = float(expenses.aggregate(Sum('amount'))['amount__sum'] or 0)
#     remaining_budget = total_budget - total_expenses

#     return render(request, 'expense/1report.html', {
#         'categories': categories,
#         'selected_category': selected_category,
#         'total_budget': total_budget,
#         'total_expenses': total_expenses,
#         'remaining_budget': remaining_budget,
#         'expense_labels': json.dumps(labels),
#         'expense_data': json.dumps(data),
#     })


import json
from collections import defaultdict
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.db.models import Sum
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import Expense, Budget  

@login_required
def report_view(request):
    categories = Expense.CATEGORY  # Fetch categories from the model
    selected_category = request.GET.get('category', '')  # Get selected category from query params

    # Get current month range
    today = now().date()
    start_of_month = today.replace(day=1)  # First day of the current month

    # Filter expenses by user and current month
    expenses = Expense.objects.filter(user=request.user, date__gte=start_of_month)
    
    if selected_category:
        expenses = expenses.filter(category=selected_category)

    # Group expenses by date
    grouped_expenses = defaultdict(list)
    for expense in expenses:
        grouped_expenses[expense.date].append(expense)

    # Create a list with totals
    expenses_with_totals = [
        {
            "date": date,
            "expenses": grouped_expenses[date],
            "total": sum(exp.amount for exp in grouped_expenses[date]),
        }
        for date in sorted(grouped_expenses.keys(), reverse=True)
    ]

    # Aggregate expenses per category and convert to float
    category_expense_data = expenses.values('category').annotate(total=Sum('amount'))
    labels = [entry['category'] for entry in category_expense_data]
    data = [float(entry['total']) for entry in category_expense_data]  # Convert Decimal to float

    # Budget calculations
    budgets = Budget.objects.filter(user=request.user)
    if selected_category:
        budgets = budgets.filter(category=selected_category)

    total_budget = float(budgets.aggregate(Sum('amount'))['amount__sum'] or 0)
    total_expenses = float(expenses.aggregate(Sum('amount'))['amount__sum'] or 0)
    remaining_budget = total_budget - total_expenses

    return render(request, 'expense/2report.html', {
        'categories': categories,
        'selected_category': selected_category,
        'total_budget': total_budget,
        'total_expenses': total_expenses,
        'remaining_budget': remaining_budget,
        'expenses_with_totals': expenses_with_totals,
        'expense_labels': json.dumps(labels),
        'expense_data': json.dumps(data),
    })

@login_required
def export_report_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="expense_report.pdf"'
    
    p = canvas.Canvas(response)
    p.drawString(100, 800, "Expense Report")
    
    today = now().date()
    start_of_month = today.replace(day=1)
    expenses = Expense.objects.filter(user=request.user, date__gte=start_of_month)
    y_position = 780
    
    for expense in expenses:
        p.drawString(100, y_position, f"{expense.date}: {expense.category} - {expense.amount}")
        y_position -= 20
        if y_position < 50:
            p.showPage()
            y_position = 800
    
    p.showPage()
    p.save()
    return response


# import json
# import matplotlib.pyplot as plt
# from collections import defaultdict
# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from django.utils.timezone import now
# from django.db.models import Sum
# from django.http import HttpResponse
# from reportlab.pdfgen import canvas
# from reportlab.lib.utils import ImageReader
# from io import BytesIO
# from .models import Expense, Budget  

# @login_required
# def export_report_chart_pdf(request):
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="expense_report_chart.pdf"'
    
#     p = canvas.Canvas(response)
#     p.drawString(100, 800, "Expense Report with Chart")
    
#     today = now().date()
#     start_of_month = today.replace(day=1)
#     expenses = Expense.objects.filter(user=request.user, date__gte=start_of_month)

#     y_position = 780
#     for expense in expenses:
#         p.drawString(100, y_position, f"{expense.date}: {expense.category} - {expense.amount}")
#         y_position -= 20
#         if y_position < 350:  # Ensure enough space for the chart
#             p.showPage()
#             y_position = 800

#     # Generate Pie Chart
#     category_expense_data = expenses.values('category').annotate(total=Sum('amount'))
#     labels = [entry['category'] for entry in category_expense_data]
#     data = [float(entry['total']) for entry in category_expense_data]

#     if data:  # Only generate chart if there is data
#         fig, ax = plt.subplots(figsize=(5, 5))  # Keep the chart aspect ratio square
#         ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=140)
#         plt.axis('equal')

#         img_buffer = BytesIO()
#         plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=100)  # Improve resolution
#         plt.close(fig)

#         img_buffer.seek(0)
#         img = ImageReader(img_buffer)

#         # Ensure aspect ratio is preserved
#         p.drawImage(img, 120, 100, width=300, height=300, preserveAspectRatio=True, mask='auto')

#     p.showPage()
#     p.save()
#     return response

import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.platypus import Image

from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.db.models import Sum
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from .models import Expense

@login_required
def export_report_chart_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="monthly_expense_report.pdf"'
    
    # Create PDF document
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph("Monthly Expense Report", styles['Title']))
    elements.append(Spacer(1, 12))

    # Get expenses for the current month
    today = now().date()
    start_of_month = today.replace(day=1)
    expenses = Expense.objects.filter(user=request.user, date__gte=start_of_month)

    if not expenses.exists():
        elements.append(Paragraph("No expenses recorded this month.", styles['Normal']))
        doc.build(elements)
        return response  # Ensure response is always returned

    # Organize data for the table
    data = [["Date", "Details", "Total"]]
    expense_data = {}

    for expense in expenses:
        date_str = expense.date.strftime("%B %d, %Y")
        if date_str not in expense_data:
            expense_data[date_str] = []
        expense_data[date_str].append(f"{expense.category}: {expense.amount:.2f}")

    for date, details in expense_data.items():
        total = sum(float(d.split(": ")[-1]) for d in details)
        details_paragraph = Paragraph("<br/>".join(f"• {d}" for d in details), styles['Normal'])
        data.append([date, details_paragraph, f"{total:.2f}"])

    # Create and style the table
    table = Table(data, colWidths=[100, 300, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (1, 1), (-1, -1), 'TOP'),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 24))

    # Generate Pie Chart
    category_expense_data = expenses.values('category').annotate(total=Sum('amount'))
    labels = [entry['category'] for entry in category_expense_data]
    amounts = [float(entry['total']) for entry in category_expense_data]

    if amounts:  # Only generate chart if there is data
        fig, ax = plt.subplots(figsize=(6, 6))  # Ensure a square figure
        wedges, texts, autotexts = ax.pie(
            amounts, labels=labels, autopct='%1.1f%%', startangle=140, 
            colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']
        )
        ax.set_aspect('equal')  # Ensures equal proportions
        plt.title("Expense Breakdown using Pie-Chart", fontsize=14, fontweight='bold')

        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)  # High resolution
        plt.close(fig)
        img_buffer.seek(0)

        # Insert Pie Chart
        img = Image(img_buffer, width=300, height=300)  # Keep proportions
        elements.append(Spacer(1, 24))
        elements.append(img)

    doc.build(elements)
    return response
