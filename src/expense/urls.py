from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.expense_list, name='expense_list'),
    path('addexpense/', views.add_expense, name='add_expense'),
    path('showcategory', views.category_list, name='category_list'),
    path('addcategory/', views.add_category, name='add_category'),
    path('updateexpense/<int:expense_id>', views.update_expense, name='updateexpense'),
    path('deleteexpense/<int:expense_id>', views.delete_expense, name='deleteexpense'),
    path('updatecategory/<int:category_id>', views.update_category, name='updatecategory'),
    path('deletecategory/<int:category_id>', views.delete_category, name='deletecategory'),
]
