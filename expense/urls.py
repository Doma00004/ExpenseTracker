from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # category
    # path('showcategory', views.category_list, name='category_list'),
    # path('addcategory/', views.add_category, name='add_category'),
    # path('updatecategory/<int:category_id>', views.update_category, name='updatecategory'),
    # path('deletecategory/<int:category_id>', views.delete_category, name='deletecategory'),

    # expense 
    path('showexpense/', views.expense_list, name='expense_list'),
    path('addexpense/', views.add_expense, name='add_expense'),
    path('updateexpense/<int:expense_id>', views.update_expense, name='updateexpense'),
    path('deleteexpense/<int:expense_id>', views.delete_expense, name='deleteexpense'),
    
    # budget
    path('showbudget', views.budget_list, name='budget_list'),
    path('addbudget/', views.add_budget, name='add_budget'),
    path('updatebudget/<int:budget_id>', views.update_budget, name='updatebudget'),
    path('deletebudget/<int:budget_id>', views.delete_budget, name='deletebudget'),
    path('report/', views.report, name='report'),
]
