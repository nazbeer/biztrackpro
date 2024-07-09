from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Define the list of exempt URLs that do not require authentication
        self.exempt_urls = [
            reverse('login'),
            reverse('expense_report_api'),
            reverse('daily_collection_report_api'),
            reverse('sales_report'),
            reverse('purchase_report'),
            reverse('msc_income_report'),
            reverse('supplier_payment_report'),
            reverse('bank_statement'),
            reverse('customer_payment_report'),
            reverse('expense_report_pdf'),
            reverse('bank-statement-pdf'),
            reverse('daily-report-pdf'),
            reverse('supplier-payment-report-pdf'),
            reverse('customer-payment-report-pdf'),
            reverse('passDS'),
            reverse('daily_summary_exists'),
            reverse('api_login')
        ]

    def __call__(self, request):
        if not request.user.is_authenticated and request.path not in self.exempt_urls:
            messages.error(request, 'Please login to continue')
            return redirect('login')
        response = self.get_response(request)
        return response