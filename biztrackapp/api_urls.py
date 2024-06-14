# your_app_name/api_urls.py
from django.urls import path
from .views import (
    DailyCollectionReportAPIView, SalesReportAPIView, PurchaseReportAPIView,
    MscIncomeReportAPIView, SupplierPaymentReportAPIView, BankStatementAPIView,
    BankStatementPDFView, DailyCollectionReportPDFView, PassDSDailySummaryAPIView
)

custom_api_urls = [
    path('daily-collection-report/', DailyCollectionReportAPIView.as_view(), name='daily_collection_report_api'),
    path('sales-report/', SalesReportAPIView.as_view(), name='sales_report'),
    path('purchase-report/', PurchaseReportAPIView.as_view(), name='purchase_report'),
    path('msc-income-report/', MscIncomeReportAPIView.as_view(), name='msc_income_report'),
    path('supplier-payment-report/', SupplierPaymentReportAPIView.as_view(), name='supplier_payment_report'),
    path('bank-statement/', BankStatementAPIView.as_view(), name='bank_statement'),
    # path('bank-statement-pdf/', BankStatementPDFView.as_view(), name='bank-statement-pdf'),
    # path('daily-report-pdf/', DailyCollectionReportPDFView.as_view(), name='daily-report-pdf'),
    # path('passDS/', PassDSDailySummaryAPIView.as_view(), name='passDS'),
]

urlpatterns = custom_api_urls
