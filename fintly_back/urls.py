from django.urls import path

from . import views

urlpatterns = [
    
    path('monthlycategories/', views.montlhy_categories,
         name='monthly_categories'),
    
    path('updatetransactions/', views.upload_transactions_to_db,
         name='updatetransactions'),
    
    path('monthlyexpenses/', views.monthly_expenses,
         name='monthly_expenses'),
    
    path('monthlyexpenses/<str:month>', views.monthly_expenses,
         name='monthly_expenses'),
    
    path('monthlyincomes/', views.monthly_incomes,
         name='monthly_incomes'),
    
     path('monthlyincomes/<str:month>', views.monthly_incomes,
         name='monthly_incomes'),
    
    path('expenseslist/', views.expenses_list_by_month,
         name='expenseslist'),
    
    path('getdistinctcategory/', views.get_expenses_category_list,
         name='getDistinctCategory'),
    
    path('balances/', views.get_user_balances,
         name='balances'),
    
    path('transaction/', views.is_transaction,
         name='transaction'),

    path('link/', views.user_links,
         name='link'),
    

]
