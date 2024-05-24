from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from .views import *
from biztrackapp import views

urlpatterns = [

    path('',login_view,name='login' ),
    path('logout/',logout_view,name='logout' ),
    path('home/',HomeView.as_view(),name='home' ),
    path('create-business-profile/', create_business_profile, name='create_business_profile'),
    path('business/', business_profile_list, name='business_profile_list'),
    path('business_profiles/<int:pk>/edit/', edit_business_profile, name='edit_business_profile'),
    path('business_profiles/<int:pk>/delete/', delete_business_profile, name='delete_business_profile'),

    path('expense-type/', ExpenseTypeListView.as_view(), name='expense_type_list'),
    path('expense-type/create/', create_expense_type, name='create_expense_type'),
    path('expense-type/<int:pk>/edit/', ExpenseTypeUpdateView.as_view(), name='edit_expense_type'),
    path('expense-type/<int:pk>/delete/', ExpenseTypeDeleteView.as_view(), name='delete_expense_type'),
 
    path('receipt-type/create/', create_receipt_type, name='create_receipt_type'),
    path('receipt-type/', receipt_type_list, name='receipt_type_list'),
    path('receipt-type/<int:pk>/edit/', ReceiptTypeUpdateView.as_view(), name='edit_receipt_type'),

    path('mode-transaction/', ModeOfTransaction.as_view(), name='mode_of_transaction_list'),
    path('mode-transaction/create/', create_mode_of_transaction, name='create_mode_of_transaction'),
    path('mode-transaction/<int:pk>/edit/', ModeofTransactionUpdateView.as_view(), name='edit_mode_of_transaction'),

    path('create-business-timing/', create_business_timing, name='create_business_timing'),
    path('business-timing-list/', business_timing_list, name='business_timing_list'),

    path('bank/create/', create_bank, name='create_bank'),
    path('banks/', BankListView.as_view(), name='bank_list'),

    path('employee/', employee_list, name='employee_list'),
    path('employee/create/', create_employee, name='create_employee'),
    path('employees/<int:pk>/edit/', employee_edit, name='employee_edit'),


    path('create-supplier/', create_supplier, name='create_supplier'),
    path('create-customer/', create_customer, name='create_customer'),
    path('customer-list/', customer_list, name='customer_list'),
    path('supplier-list/', supplier_list, name='supplier_list'),

    path('success/', success_view, name='success'),

    path('daily-summary/', daily_summary_list, name='daily_summary_list'),
    path('daily-summary/create/', create_daily_summary, name='create_daily_summary'),
    
    path('bank-sale/create/', create_bank_sale, name='create_bank_sale'),
    path('bank-sales/', list_bank_sales, name='list_bank_sales'),

    path('create-credit-collection/', create_credit_collection, name='create_credit_collection'),
    path('credit-collections/', list_credit_collection, name='list_credit_collection'),

    path('create-misc-income/', create_misc_income, name='create_misc_income'),
    path('misc-income/', list_msc_income, name='list_msc_income'),

    path('create_purchase/', create_purchase, name='create_purchase'),
    path('purchases/', list_purchases, name='list_purchases'),


    path('create_supplier_payment/', create_supplier_payment, name='create_supplier_payment'),
    path('supplier_payments/', list_supplier_payment, name='list_supplier_payment'),

    

]
# handler404 = 'custom_404_view'
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)