from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from .views import *
from biztrackapp import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="BizTrackPro API",
        default_version='v1',
        description="Developed by Nasbeer Ahammed",
        terms_of_service="https://www.tickets2me.com/index.php/privacy-policy-2/",
        contact=openapi.Contact(email="info@mitesolutions.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [

    #api routers and swagger
    path('api/', include('biztrackapp.api_urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('readoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # Optional Redoc UI


    path('edit/',save_after_submit,name='save_after_submit' ),
    path('get_closing_balance/<str:id>/',get_daily_summary_data,name='get_closing_balance' ),
    path('get_supplier_outstanding/<int:id>/',get_supplier_outstanding,name='get_supplier_outstanding' ),
    path('get_customer_outstanding/<int:id>/',get_customer_outstanding,name='get_customer_outstanding' ),
    
    path('edit_bank_sale/<int:pk>/',edit_bank_sale,name='edit_bank_sale' ),
    path('edit_credit_collection/<int:pk>/',edit_credit_collection,name='edit_credit_collection'),
    path('edit_miscellaneous_income/<int:pk>/',edit_miscellaneous_income,name='edit_miscellaneous_income'),
    path('edit_withdrawal/<int:pk>/',edit_withdrawal,name='edit_withdrawal'),
    path('edit_purchase/<int:pk>/',edit_purchase,name='edit_purchase'),
    path('edit_supplier_payment/<int:pk>/',edit_supplier_payment,name='edit_supplier_payment'),
    path('edit_expense/<int:pk>/',edit_expense,name='edit_expense'),
    path('edit_bank_deposit/<int:pk>/',edit_bank_deposit,name='edit_bank_deposit'),

    path('delete_bank_sale/<int:pk>/',delete_bank_sale,name='delete_bank_sale'),
    path('delete_credit_collection/<int:pk>/',delete_credit_collection,name='delete_credit_collection'),
    path('delete_miscellaneous_income/<int:pk>/',delete_miscellaneous_income,name='delete_miscellaneous_income'),
    path('delete_withdrawal/<int:pk>/',delete_withdrawal,name='delete_withdrawal'),
    path('delete_purchase/<int:pk>/',delete_purchase,name='delete_purchase'),
    path('delete_supplier_payment/<int:pk>/',delete_supplier_payment,name='delete_supplier_payment'),
    path('delete_expense/<int:pk>/',delete_expense,name='delete_expense'),
    path('delete_bank_deposit/<int:pk>/',delete_bank_deposit,name='delete_bank_deposit'),


    path('create_all_banks/', create_all_banks, name='create_all_banks'),

    path('',login_view,name='login' ),
    path('logout/',logout_view,name='logout' ),
    path('home/',HomeView.as_view(),name='home' ),
    path('create-business-profile/', create_business_profile, name='create_business_profile'),
    path('business/', business_profile_list, name='business_profile_list'),
    path('business_profiles/<int:pk>/edit/', edit_business_profile, name='edit_business_profile'),
    path('business_profiles/<int:pk>/delete/', delete_business_profile, name='delete_business_profile'),

    path('partners/', PartnerListView.as_view(), name='partner_list'),
    path('partners/create/', PartnerCreateView.as_view(), name='partner_create'),

    path('withdrawals/', list_withdrawal, name='withdrawal_list'),
    path('withdrawals/create/', create_withdrawal, name='withdrawal_create'),

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
    path('business_timing/edit/<int:id>/', edit_business_timing, name='edit_business_timing'),
    path('business_timing/delete/<int:id>/', delete_business_timing, name='delete_business_timing'),
   
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
    path('create-daily-summary/', create_daily_summary, name='create_daily_summary'),
    path('daily_summary/edit/<int:id>/', edit_daily_summary, name='edit_daily_summary'),
    path('daily_summary/delete/<int:pk>/', delete_daily_summary, name='delete_daily_summary'),
    
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

    path('create-bank-deposit/', create_bank_deposit, name='create_bank_deposit'),
    path('bank-deposit/', list_bank_deposit, name='list_bank_deposit'),

    path('create-expense/', create_expense, name='create_expense'),
    path('list-expense/', list_expense, name='list_expense'),

    path('fetch_cheque_numbers/', fetch_cheque_numbers, name='fetch_cheque_numbers'),

    path('daily-collection-report/', DailyCollectionReportView.as_view(), name='daily_collection_report'),
    path('sales-report/', SalesReportView.as_view(), name='sales_report'),
    path('purchase-report/', PurchaseReportView.as_view(), name='purchase_report'),
    path('msc-income-report/', MscIncomeReportView.as_view(), name='msc_income_report'),
    path('supplier-payment-report/', SupplierPaymentReportView.as_view(), name='supplier_payment_report'),
    path('bank-statement/', BankStatementView.as_view(), name='bank_statement'),


    # path('download-pdf-cc/', download_pdf_cc, name='download_pdf_cc'),
    #API Views

    path('api/daily-collection-report/', DailyCollectionReportAPIView.as_view(), name='daily_collection_report_api'),
    path('api/sales-report/', SalesReportAPIView.as_view(), name='sales_report'),
    path('api/purchase-report/', PurchaseReportAPIView.as_view(), name='purchase_report'),
    path('api/msc-income-report/', MscIncomeReportAPIView.as_view(), name='msc_income_report'),
    path('api/supplier-payment-report/', SupplierPaymentReportAPIView.as_view(), name='supplier_payment_report'),
    path('api/bank-statement/', BankStatementAPIView.as_view(), name='bank_statement'),
    path('api/bank-statement-pdf/', BankStatementPDFView.as_view(), name='bank-statement-pdf'),
    path('api/daily-report-pdf/', DailyCollectionReportPDFView.as_view(), name='daily-report-pdf'),
    path('api/supplier-payment-report-pdf/', SupplierPaymentReportPDFAPIView.as_view(), name='supplier-payment-report-pdf'),

    path('api/passDS/', PassDSDailySummaryAPIView.as_view(), name='passDS'),
    path('api/daily_summary_exists/', CheckDailySummaryExists.as_view(), name='daily_summary_exists'),
]
# handler404 = 'custom_404_view'
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)