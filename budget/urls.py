from django.urls import path
from budget.views import BudgetList, BudgetDetail, ExpenseList, ExpenseDetail, BudgetListFilter, ExpensesListFilter

urlpatterns = [
    path('', BudgetList.as_view(), name='budget-list'),
    path('filter/', BudgetListFilter.as_view(), name='budget-filter'),
    path('<int:pk>/', BudgetDetail.as_view(), name='budget-single'),
    path('<int:budget_id>/expenses/', ExpenseList.as_view(), name='expense-list'),
    path('<int:budget_id>/expenses/filter/', ExpensesListFilter.as_view(), name='expense-filter'),
    path('<int:budget_id>/expenses/<int:pk>/', ExpenseDetail.as_view(), name='expense-single'),
]
  