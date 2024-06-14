from django.shortcuts import render, redirect,HttpResponse,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.views.generic import TemplateView,ListView
from django.template.loader import get_template
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse,reverse_lazy
from .forms import *
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.db.models import Count, Sum, Q, F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from django.http import JsonResponse, HttpResponse

from django.views import View
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.template.loader import render_to_string
# from weasyprint import HTML
import tempfile
from rest_framework.request import Request


def index(request):
    print('re',request.user)
    user = request.user
    business = ShopAdmin.objects.get(user = user)
    return HttpResponse(f"{user}  {business}")

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print('usser',user)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')
    

def logout_view(request):
    logout(request)
    return redirect('login') 
 
def success_view(request):
    return render(request, 'success.html')



class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            try:
                shop_admin = ShopAdmin.objects.get(user=self.request.user)
                context['shop'] = shop_admin.shop
                context['user'] = shop_admin.user


            except ShopAdmin.DoesNotExist:
                # Render the template with a message
                context['error_message'] = "No shop associated with the current user."
                
        categories = [
            
            {
                'name': 'Shop Management',
                'links': [
                    {'label': 'Create Business', 'url_name': 'create_business_profile'},
                    {'label': 'Business Profiles', 'url_name': 'business_profile_list'},
                ]
            },
            {
                'name': 'Partner Management',
                'links': [
                    {'label': 'Create Partners', 'url_name': 'partner_create'},
                    {'label': 'Partner List', 'url_name': 'partner_list'},
                   
                ]
            },
            {
                'name': 'Employee Management',
                'links': [
                        {'label': 'Create Employee', 'url_name': 'create_employee'},
                        {'label': 'Employee List', 'url_name': 'employee_list'},
                  
                ]
            },
        ]

        context['categories'] = categories
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Redirect to login page if user is not logged in
            return redirect(reverse('login'))  # Adjust 'login' to your login URL name
        return super().dispatch(request, *args, **kwargs)
    

def create_business_profile(request):
    error_occurred = False  

    if request.method == 'POST':
        business_profile_form = BusinessProfileForm(request.POST, request.FILES)
        if business_profile_form.is_valid():
            business_profile = business_profile_form.save(commit=False)
            # shop_admin = ShopAdmin.objects.get(user=request.user)
            business_profile.save()
            return redirect('success')
        else:
            # Form is not valid, display form with errors
            messages.error(request, "Please correct the errors below.")
    else:
        business_profile_form = BusinessProfileForm()

    context = {'business_profile_form': business_profile_form}
    if request.user.is_authenticated:
        # Fetch the shop details associated with the logged-in user
        try:
            shop_admin = ShopAdmin.objects.get(user=request.user)
            shop_name = shop_admin.shop.name
            # print(shop_name)
            context['shop_details'] = shop_admin.shop
            context['license_number'] = shop_admin.shop.license_number

            # Check if a business profile already exists with the same name as shop name
            if BusinessProfile.objects.filter(name=shop_name).exists():
                context['disable_submit'] = True  # Disable submit button
                # messages.info(request, "Only one business profile can be created under a shop.")
        except ShopAdmin.DoesNotExist:
            context['shop_details'] = None
            context['license_number'] = None

    return render(request, 'create_business_profile.html', context)

def business_profile_list(request):
    context = {}
    if request.user.is_authenticated:
        try:
            # Fetch the shop details associated with the logged-in user
            shop_admin = ShopAdmin.objects.get(user=request.user)
            # shop_name = shop_admin.shop.name
            shop = shop_admin.shop

            
            # Filter Business Profiles based on the logged-in user's shop name
            profiles = BusinessProfile.objects.filter(name=shop.name)
            context['profiles'] = profiles
            context['shop_details'] = shop_admin.shop
            context['license_number'] = shop_admin.shop.license_number
        except ShopAdmin.DoesNotExist:
            context['profiles'] = None
            context['shop_details'] = None
            context['license_number'] = None
    else:
        # If user is not authenticated, set profiles to None
        context['profiles'] = None

    return render(request, 'business_profile_list.html', context)


def edit_business_profile(request, pk):
    business_profile = get_object_or_404(BusinessProfile, pk=pk)
    if request.method == 'POST':
        form = BusinessProfileForm(request.POST, request.FILES, instance=business_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Business profile updated successfully.')
            return redirect('business_profile_list')
    else:
        form = BusinessProfileForm(instance=business_profile)
    return render(request, 'edit_business_profile.html', {'form': form, 'business_profile': business_profile})

def delete_business_profile(request, pk):
    business_profile = get_object_or_404(BusinessProfile, pk=pk)
    if request.method == 'POST':
        business_profile.delete()
        messages.success(request, 'Business profile deleted successfully.')
        return redirect('business_profile_list')
    return render(request, 'delete_business_profile.html', {'business_profile': business_profile})

from django.contrib.auth.mixins import LoginRequiredMixin
class PartnerListView(LoginRequiredMixin, View):
    def get(self, request):
        shop = Shop.objects.filter(shopadmin__user=request.user).first()
        if shop:
            partners = Partners.objects.filter(shop=shop)
        else:
            partners = Partners.objects.none()
        return render(request, 'partner_list.html', {'partners': partners})

class PartnerCreateView(LoginRequiredMixin, View):
    def get(self, request):
        shop = Shop.objects.filter(shopadmin__user=request.user).first()
        form = PartnerForm(initial={'shop': shop})
        return render(request, 'partner_form.html', {'form': form})

    def post(self, request):
        shop = Shop.objects.filter(shopadmin__user=request.user).first()
        form = PartnerForm(request.POST, initial={'shop': shop})
        if form.is_valid():
            partner = form.save(commit=False)
            partner.shop = shop
            partner.save()
            return redirect(reverse('partner_list'))
        return render(request, 'partner_form.html', {'form': form})
def create_supplier(request):
    shop_admin = get_object_or_404(ShopAdmin, user=request.user)
    
    # Get the shop associated with the shop admin
    shop = shop_admin.shop.name
    
    # Get the business profile associated with the shop
    # business_profile = get_object_or_404(BusinessProfile, name=shop.name)
    business_profile = get_object_or_404(BusinessProfile, name=shop)

  
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save(commit=False)
            supplier.business_profile = business_profile.id
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'create_supplier.html', {'form': form, 'business_profile': business_profile.id})

def create_customer(request):
    shop_admin = get_object_or_404(ShopAdmin, user=request.user)
    # Get the shop associated with the shop admin
    shop = shop_admin.shop
    # Get the business profile associated with the shop
    business_profile = get_object_or_404(BusinessProfile, name=shop.name)
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.business_profile = business_profile.id
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'create_customer.html', {'form': form, 'business_profile': business_profile.id})


def customer_list(request):
    try:
        shop_admin = ShopAdmin.objects.get(user=request.user)
        shop = shop_admin.shop
        business = BusinessProfile.objects.get(license_number=shop.license_number)
    except ShopAdmin.DoesNotExist:
        return redirect('login')
    except BusinessProfile.DoesNotExist:
        business = None
        
    customers = Customer.objects.filter(business_profile=business.id).order_by('-created_on')
    return render(request, 'customer-list.html', {'customers': customers})


def supplier_list(request):
    try:
        shop_admin = ShopAdmin.objects.get(user=request.user)
        shop = shop_admin.shop
        business = BusinessProfile.objects.get(license_number=shop.license_number)
    except ShopAdmin.DoesNotExist:
        return redirect('login')
    except BusinessProfile.DoesNotExist:
        business = None
        
    suplliers = Supplier.objects.filter(business_profile=business.id).order_by('-created_on')
    return render(request, 'supplier-list.html', {'suppliers': suplliers})


def create_expense_type(request):
    try:
        # Get the current shop admin
        shop_admin = ShopAdmin.objects.get(user=request.user)
        # Get the associated shop
        shop = shop_admin.shop
        # Get the business profile associated with the shop
        business_profile = BusinessProfile.objects.get(name=shop.name)
    except BusinessProfile.DoesNotExist:
        messages.error(request, "Business profile is not created. Please create a business profile first.")
        return redirect('create_business_profile')  # Redirect to the view where you create a business profile

    if request.method == 'POST':
        form = ExpenseTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_type_list')
    else:
        form = ExpenseTypeForm()
    return render(request, 'create_expense_type.html', {'form': form,'business_profile':business_profile.id})


class ExpenseTypeListView(ListView):
    model = ExpenseType
    template_name = 'expense_type_list.html'
    def get_queryset(self):
        shop_admin = get_object_or_404(ShopAdmin, user=self.request.user)
    
        # Get the shop associated with the shop admin
        shop = shop_admin.shop
        
        # Get the business profile associated with the shop
        business_profile = get_object_or_404(BusinessProfile, name=shop.name)
        # Return the queryset of DailySummary objects sorted by date in ascending order
        return ExpenseType.objects.filter(business_profile=business_profile.id).order_by('-created_on')
    
class ExpenseTypeUpdateView(UpdateView):
    model = ExpenseType
    form_class = ExpenseTypeForm
    template_name = 'update_expense_type.html'
    success_url = reverse_lazy('expense_type_list')

class ExpenseTypeDeleteView(DeleteView):
    model = ExpenseType
    template_name = 'delete_expense_type.html'
    success_url = reverse_lazy('expense_type_list')


def create_receipt_type(request):
    try:
        # Get the current shop admin
        shop_admin = ShopAdmin.objects.get(user=request.user)
        # Get the associated shop
        shop = shop_admin.shop
        # Get the business profile associated with the shop
        business_profile = BusinessProfile.objects.get(name=shop.name)
    except BusinessProfile.DoesNotExist:
        messages.error(request, "Business profile is not created. Please create a business profile first.")
        return redirect('create_business_profile')  # Redirect to the view where you create a business profile
    
    if request.method == "POST":
        form = ReceiptTypeForm(request.POST)
        if form.is_valid():
            receipt_type= form.save(commit=False)
            receipt_type.save()
            return redirect('receipt_type_list')  
    else:
        form = ReceiptTypeForm()
    return render(request, 'create_receipt_type.html', {'form': form,'business_profile':business_profile.id})



def receipt_type_list(request):
    # Retrieve the current user's shop admin instance
    shop_admin = get_object_or_404(ShopAdmin, user=request.user)
    shop = shop_admin.shop
    
    # Retrieve the business profile associated with the shop
    business_profile = get_object_or_404(BusinessProfile, name=shop.name)
    
    # Retrieve the receipt types associated with the business profile
    receipt_types = ReceiptType.objects.filter(business_profile=business_profile.id).order_by('-created_on')
    
    # Render the template with the receipt types
    return render(request, 'receipt_type_list.html', {'object_list': receipt_types})

class ReceiptTypeUpdateView(UpdateView):
    model = ReceiptType 
    form_class = ReceiptTypeForm
    template_name = 'update_receipt_type.html'
    success_url = reverse_lazy('receipt_type_list')


def create_bank(request):
    try:
        # Get the current shop admin
        shop_admin = ShopAdmin.objects.get(user=request.user)
        # Get the associated shop
        shop = shop_admin.shop
        # Get the business profile associated with the shop
        business_profile = BusinessProfile.objects.get(name=shop.name)
    except BusinessProfile.DoesNotExist:
        messages.error(request, "Business profile is not created. Please create a business profile first.")
        return redirect('create_business_profile')  # Redirect to the view where you create a business profile

    if request.method == 'POST':
        form = BankForm(request.POST)
        if form.is_valid():
            bank = form.save(commit=False)
            bank.business_profile = business_profile.id  # Link to the business profile
            bank.save()
            return redirect('bank_list')  
    else:
        form = BankForm()

    context = {
        'form': form,
        'business_profile': business_profile.id,
        # 'bank_choices': BANK_CHOICES
    }
    return render(request, 'create_bank.html', context)

class BankListView(ListView):
    model = Bank
    template_name = 'bank_list.html'
    
    def get_queryset(self):
        shop_admin = get_object_or_404(ShopAdmin, user=self.request.user)
    
        # Get the shop associated with the shop admin
        shop = shop_admin.shop
        
        # Get the business profile associated with the shop
        business_profile = get_object_or_404(BusinessProfile, name=shop.name)
    
        # Return the queryset of Bank objects filtered by business profile and sorted by created_on date in descending order
        return Bank.objects.filter(business_profile=business_profile.id).order_by('-created_on')



def create_mode_of_transaction(request):
    choices = TransactionMode.CHOICES  # Accessing the choices from the model
    try:
        # Get the current shop admin
        shop_admin = ShopAdmin.objects.get(user=request.user)
        # Get the associated shop
        shop = shop_admin.shop
        # Get the business profile associated with the shop
        business_profile = BusinessProfile.objects.get(name=shop.name)
    except BusinessProfile.DoesNotExist:
        messages.error(request, "Business profile is not created. Please create a business profile first.")
        return redirect('create_business_profile')  # Redirect to the view where you create a business profile
    
    if request.method == 'POST':
        form = ModeofTransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mode_of_transaction_list')  
    else:
        form = ModeofTransactionForm()

    context = {
        'form': form,
        'business_profile': business_profile.id,
        'transaction_modes':choices   
    }
    return render(request, 'create_mode_transaction.html', context)


class ModeOfTransaction(ListView):
    model = TransactionMode
    template_name = 'mode_transaction_list.html'
    
    def get_queryset(self):
        shop_admin = get_object_or_404(ShopAdmin, user=self.request.user)
    
        # Get the shop associated with the shop admin
        shop = shop_admin.shop
        
        # Get the business profile associated with the shop
        business_profile = get_object_or_404(BusinessProfile, name=shop.name)
    
        # Return the queryset of Bank objects filtered by business profile and sorted by created_on date in descending order
        return TransactionMode.objects.filter(business_profile=business_profile.id).order_by('-created_on')

class ModeofTransactionUpdateView(UpdateView):
    model = TransactionMode 
    form_class = ModeofTransactionForm
    template_name = 'update_mode_of_transaction.html'
    success_url = reverse_lazy('mode_of_transaction_list')


def create_employee(request):
    error_occurred = False  
    try:
        # Get the current shop admin
        shop_admin = ShopAdmin.objects.get(user=request.user)
        # Get the associated shop
        shop = shop_admin.shop
        # Get the business profile associated with the shop
        BusinessProfile.objects.get(name=shop.name)
    except BusinessProfile.DoesNotExist:
        messages.error(request, "Business profile is not created. Please create a business profile first.")
        return redirect('create_business_profile')  # Redirect to the view where you create a business profile

    # Fetch the shop details associated with the logged-in user
    try:
        shop_admin = ShopAdmin.objects.get(user=request.user)
        shop = shop_admin.shop
    except ShopAdmin.DoesNotExist:
        shop = None

    if shop:
        num_users = shop.num_users
        # Check the number of users created under this shop
        num_users_created = Employee.objects.filter(business_profile=shop).count()
        
        # Pass the maximum allowed users count to the template
        max_users_allowed = num_users
      
    business_profiles = BusinessProfile.objects.filter(name=shop)
        
        # Filter roles based on the business profile
    # roles = Role.objects.filter(business_profile=business_profile)
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            if num_users_created >= max_users_allowed:
                # If the maximum limit is reached, display an error message
                error_occurred = True
                messages.error(request, "Max User Registration limit is reached.")
            else:
                try:
                    employee = form.save(commit=False)
                    # employee.business_profile_id = request.POST.get('business_profile_id')  # Set business_profile_id from POST data
                    employee.save()
                    return HttpResponse('employee_list') 
                except Exception as e:
                    # print("An error occurred while saving the form:", e)
                    error_occurred = True  
                    messages.error(request, "An error occurred while saving the form.")
    else:
        form = EmployeeForm()

    # Filter Business Profiles based on the shop associated with the logged-in user
    

    context = {
    'form': form,
    # 'roles':roles,
    'business_profiles': business_profiles,
    'error_occurred': error_occurred,
    'num_users_created': num_users_created,
    'max_users_allowed': max_users_allowed,
    'business_profile_id': shop.id,
    }

    return render(request, 'create_employee.html', context)



def employee_list(request):
    # Get the shop admin user
    shop_admin = get_object_or_404(ShopAdmin, user=request.user)
    
    # Get the shop associated with the shop admin
    shop = shop_admin.shop

    # Get the business profile associated with the shop
    business_profile = shop

    query = request.GET.get('q')
    if query:
        employees = Employee.objects.filter(
            Q(employee_id__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query),
            business_profile=business_profile,
            # shop=shop
        )
    else:
        employees = Employee.objects.filter(business_profile=business_profile)

    paginator = Paginator(employees, 10)
    page = request.GET.get('page')
    try:
        employees = paginator.page(page)
    except PageNotAnInteger:
        employees = paginator.page(1)
    except EmptyPage:
        employees = paginator.page(paginator.num_pages)

    return render(request, 'employee_list.html', {'employees': employees})


def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employee_edit.html', {'form': form})


def daily_summary_list(request):
    today = date.today()
    shop_admin = get_object_or_404(ShopAdmin, user=request.user)
    shop = shop_admin.shop
    
    # Retrieve the business profile associated with the shop
    business_profile = get_object_or_404(BusinessProfile, name=shop.name)
    daily_summaries = DailySummary.objects.filter(business_profile=business_profile.id)
    return render(request, 'daily_summary_list.html', {'daily_summaries': daily_summaries,'today':today})

def edit_daily_summary(request, id):
    daily_summaries = get_object_or_404(DailySummary, id=id)
    print(daily_summaries)
    if request.method == 'POST':
        form = DailySummaryForm(request.POST, instance=daily_summaries)
        if form.is_valid():
            form.save()
            return redirect('daily_summary_list')
    else:
        form = DailySummaryForm(instance=daily_summaries)
    
    return render(request, 'edit_daily_summary.html', {'daily_summaries': daily_summaries, 'form': form})

def delete_daily_summary(request, pk):
    daily_summary = get_object_or_404(DailySummary, id=pk)
    print(daily_summary)
    daily_summary.delete()
    return redirect('daily_summary_list')

def create_business_timing(request):
    if request.method == 'POST':
        form = BusinessTimingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('business_timing_list')
    else:
        form = BusinessTimingForm()
    shop_admin = get_object_or_404(ShopAdmin, user=request.user)
    shop = shop_admin.shop
    
    # Retrieve the business profile associated with the shop
    business_profile = get_object_or_404(BusinessProfile, name=shop.name)
    return render(request, 'create_business_timing.html', {'form': form, 'business_profile':business_profile.id})

def business_timing_list(request):
    # Get the ShopAdmin instance for the current user
    shop_admin = get_object_or_404(ShopAdmin, user=request.user)
    
    # Retrieve the BusinessProfile instance associated with the shop
    business_profile = get_object_or_404(BusinessProfile, name=shop_admin.shop.name)
    
    # Fetch the BusinessTiming objects related to the business profile
    business_timings = BusinessTiming.objects.filter(business_profile=business_profile)
    
    # Render the business_timing_list template with the business timings
    return render(request, 'business_timing_list.html', {'business_timings': business_timings})


def edit_business_timing(request, id):
    business_timing = get_object_or_404(BusinessTiming, id=id)
    shop_admin = get_object_or_404(ShopAdmin, user=request.user)
    
    # Retrieve the BusinessProfile instance associated with the shop
    business_profile = get_object_or_404(BusinessProfile, name=shop_admin.shop.name)
    # print(business_timing)
    if request.method == 'POST':
        form = BusinessTimingForm(request.POST, instance=business_timing)
        if form.is_valid():
            form.save()
            return redirect('business_timing_list')
    else:
        form = BusinessTimingForm(instance=business_timing)
    
    return render(request, 'edit_business_timing.html', {'business_timing': business_timing, 'form': form, 'business_profile':business_profile.id})


def delete_business_timing(request, id):
    business_timing = get_object_or_404(BusinessTiming, id=id)
    print(business_timing)
    business_timing.delete()
    return redirect('business_timing_list')

from django.forms.models import model_to_dict
from decimal import Decimal
def save_after_submit(request):
    id = request.GET.get('id')
    today = date.today()
    yesterday = datetime.now() - timedelta(days=1)
    yesterday_date = yesterday.date()

    cheque_transaction_mode = None
    cash_transaction_mode = None
    bank_transaction_mode = None
    credit_transaction_mode = None
    card_transaction_mode = None

    try:
        cheque_transaction_mode = TransactionMode.objects.get(name="cheque")
    except TransactionMode.DoesNotExist:
        pass
    try:
        cash_transaction_mode = TransactionMode.objects.get(name="cash")
    except TransactionMode.DoesNotExist:
        pass
    try:
        bank_transaction_mode = TransactionMode.objects.get(name="bank transfer")
    except TransactionMode.DoesNotExist:
        pass
    try:
        credit_transaction_mode = TransactionMode.objects.get(name="credit")
    except TransactionMode.DoesNotExist:
        pass
    try:
        card_transaction_mode = TransactionMode.objects.get(name="card")
    except TransactionMode.DoesNotExist:
        pass

    shop_admin = get_object_or_404(ShopAdmin, user=request.user)
    shop = shop_admin.shop
    business_profile = get_object_or_404(BusinessProfile, name=shop.name)
    business_timing = BusinessTiming.objects.filter(business_profile=business_profile.id).first()
    daily_summary = get_object_or_404(DailySummary, daily_summary_id=id, business_profile=business_profile.id)

    if request.method == 'POST':
        form = DailySummaryForm(request.POST, instance=daily_summary)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.daily_summary_id = id
            msc_income = MiscellaneousIncome.objects.filter(business_profile=business_profile.id, daily_summary_id = id)
            purchases = Purchase.objects.filter(business_profile=business_profile.id, daily_summary_id = id)
            supplier_payments = SupplierPayments.objects.filter(business_profile=business_profile.id, daily_summary_id = id)
            expense = Expense.objects.filter(business_profile=business_profile.id, daily_summary_id = id)
            bank_sales = BankSales.objects.filter(business_profile=business_profile.id, daily_summary_id = id)
            credit_collections = CreditCollection.objects.filter(business_profile=business_profile.id, daily_summary_id = id)

            withdrawal = Withdrawal.objects.filter(business_profile=business_profile.id, daily_summary_id = id)
            withdrawal_total = withdrawal.aggregate(total_amount=Sum('amount'))['total_amount'] or 0

            total_bank_sale_amount = bank_sales.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
            bank_sale_total_credit_sales = BankSales.objects.filter(mode_of_transaction=credit_transaction_mode, daily_summary_id = id).aggregate(total_credit_amount=Sum('amount'))['total_credit_amount'] or 0


            # instance.daily_summary_id = id

            bank_sale_total_cheque_sales = BankSales.objects.filter(mode_of_transaction=cheque_transaction_mode, daily_summary_id = id).aggregate(total_cheque_amount=Sum('amount'))['total_cheque_amount'] or 0
            total_bank_sale_amount = bank_sales.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
            total_credit_sale_amount = credit_collections.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
            total_mis_income_amount = msc_income.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
            total_cash_sale = (total_bank_sale_amount  - bank_sale_total_credit_sales)

            purchase_total_cash = Purchase.objects.filter(mode_of_transaction=cash_transaction_mode, daily_summary_id = id).aggregate(total_cash_amount=Sum('invoice_amount'))['total_cash_amount'] or 0
            supplier_payment_total_cash = SupplierPayments.objects.filter(mode_of_transaction=cash_transaction_mode, daily_summary_id = id).aggregate(total_cash_amount=Sum('amount'))['total_cash_amount'] or 0
            expense_total_cash = Expense.objects.filter(mode_of_transaction=cash_transaction_mode, daily_summary_id = id).aggregate(total_cash_amount=Sum('amount'))['total_cash_amount'] or 0

            bank_deposit_total_cheque = BankDeposits.objects.filter(mode_of_transaction=cheque_transaction_mode, daily_summary_id = id).aggregate(total_cheque_amount=Sum('amount'))['total_cheque_amount'] or 0
            bank_deposit_total_cash = BankDeposits.objects.filter(mode_of_transaction=cash_transaction_mode, daily_summary_id = id).aggregate(total_cash_amount=Sum('amount'))['total_cash_amount'] or 0
            bank_deposit_total_bank = BankDeposits.objects.filter(mode_of_transaction=bank_transaction_mode, daily_summary_id = id).aggregate(total_bank_amount=Sum('amount'))['total_bank_amount'] or 0
            bank_deposit_total_card = BankDeposits.objects.filter(mode_of_transaction=card_transaction_mode, daily_summary_id = id).aggregate(total_card_amount=Sum('amount'))['total_card_amount'] or 0



            net_collection = total_cash_sale + total_credit_sale_amount + total_mis_income_amount + withdrawal_total
            net_payment = purchase_total_cash + supplier_payment_total_cash + expense_total_cash
            bank_deposit_collection = bank_deposit_total_cash + bank_deposit_total_bank + bank_deposit_total_cheque + bank_deposit_total_card
            print('net_collection',net_collection)
            print('net_payment',net_payment)
            print('bank_deposit_collection',bank_deposit_collection)
            print('withdrawal_total',withdrawal_total)

            print('opening_balance',instance.opening_balance)
            closing_balance = instance.opening_balance + net_collection - net_payment - bank_deposit_collection
            print('closing_balance',closing_balance)
            instance.closing_balance = closing_balance

            # instance.save()

            instance.save()
            status = request.POST.get('status')
            if status == "ongoing":
                # return redirect(reverse('save_after_submit'+ f'?id={instance.daily_summary_id}', args=[instance.daily_summary_id]))
                return redirect(reverse('save_after_submit') + f'?id={instance.daily_summary_id}')

            instance.status = "completed"
            return redirect('daily_summary_list')
    else:
        form = DailySummaryForm(instance=daily_summary)
        bank_sale_form = BankSaleForm()
        credit_collection_form = CreditCollectionForm()
        msc_income_form = MiscellaneousIncomeForm()
        purchase_form = PurchaseForm()
        supplier_payments_form = SupplierPaymentForm()
        bank_deposit_form = BankDepositsForm()
        expense_form = ExpenseForm()
        withdrawal_form = WithdrawalForm()

    # try:
    #     # previous_daily_summary = DailySummary.objects.get(date=yesterday_date, business_profile=business_profile.id)
    #     last_daily_summary = DailySummary.objects.filter(business_profile=business_profile.id).exclude(date=today).order_by('-date').first()
    #     bankdata = last_daily_summary.closing_balance
    #     print('yestdays bankdata', bankdata)
    # except DailySummary.DoesNotExist:
    #     bankdata = business_profile.opening_balance
    if DailySummary.objects.filter(business_profile = business_profile.id).exclude(date = today).exists():
        last_daily_summary = DailySummary.objects.filter(business_profile=business_profile.id).exclude(date=today).order_by('-date').first()
        # if last_daily_summary is not None:
        print('last_daily_summary', last_daily_summary)
        bankdata = last_daily_summary.closing_balance
        # else:
        #     last_daily_summary = business_profile.opening_balance
        #     bankdata = last_daily_summary

    else:
        last_daily_summary = business_profile.opening_balance
        bankdata = last_daily_summary



    bank_sales = BankSales.objects.filter(business_profile=business_profile.id, daily_summary_id=id)
    credit_collections = CreditCollection.objects.filter(business_profile=business_profile.id, daily_summary_id=id)
    msc_income = MiscellaneousIncome.objects.filter(business_profile=business_profile.id, daily_summary_id=id)
    purchases = Purchase.objects.filter(business_profile=business_profile.id, daily_summary_id=id)
    supplier_payments = SupplierPayments.objects.filter(business_profile=business_profile.id, daily_summary_id=id)
    expense = Expense.objects.filter(business_profile=business_profile.id, daily_summary_id=id)
    bank_deposit = BankDeposits.objects.filter(business_profile=business_profile.id, daily_summary_id=id)
    withdrawal = Withdrawal.objects.filter(business_profile=business_profile.id, daily_summary_id = id)


    expense_type = ExpenseType.objects.filter(business_profile=business_profile.id)
    receipt_type = ReceiptType.objects.filter(business_profile=business_profile.id)

    bank_sale_total_cheque_sales = BankSales.objects.filter(mode_of_transaction=cheque_transaction_mode, daily_summary_id=id).aggregate(total_cheque_amount=Sum('amount'))['total_cheque_amount'] or 0
    bank_sale_total_cash_sales = BankSales.objects.filter(mode_of_transaction=cash_transaction_mode, daily_summary_id=id).aggregate(total_cash_amount=Sum('amount'))['total_cash_amount'] or 0
    bank_sale_total_credit_sales = BankSales.objects.filter(mode_of_transaction=credit_transaction_mode, daily_summary_id=id).aggregate(total_credit_amount=Sum('amount'))['total_credit_amount'] or 0
    bank_sale_total_card_sales = BankSales.objects.filter(mode_of_transaction=card_transaction_mode, daily_summary_id=id).aggregate(total_card_amount=Sum('amount'))['total_card_amount'] or 0
    bank_sale_total_bank_sales = BankSales.objects.filter(mode_of_transaction=bank_transaction_mode, daily_summary_id=id).aggregate(total_bank_amount=Sum('amount'))['total_bank_amount'] or 0
    total_bank_sale_amount = bank_sales.aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    credit_sale_total_cheque_sales = CreditCollection.objects.filter(payment_mode=cheque_transaction_mode, daily_summary_id=id).aggregate(total_cheque_amount=Sum('amount'))['total_cheque_amount'] or 0
    credit_sale_total_cash_sales = CreditCollection.objects.filter(payment_mode=cash_transaction_mode, daily_summary_id=id).aggregate(total_cash_amount=Sum('amount'))['total_cash_amount'] or 0
    credit_sale_total_bank_sales = CreditCollection.objects.filter(payment_mode=bank_transaction_mode, daily_summary_id=id).aggregate(total_bank_amount=Sum('amount'))['total_bank_amount'] or 0
    credit_sale_total_card_sales = CreditCollection.objects.filter(payment_mode=card_transaction_mode, daily_summary_id=id).aggregate(total_card_amount=Sum('amount'))['total_card_amount'] or 0
    total_credit_sale_amount = credit_collections.aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    mis_income_total_cheque = MiscellaneousIncome.objects.filter(mode_of_transaction=cheque_transaction_mode, daily_summary_id=id).aggregate(total_cheque_amount=Sum('amount'))['total_cheque_amount'] or 0
    mis_income_total_cash = MiscellaneousIncome.objects.filter(mode_of_transaction=cash_transaction_mode, daily_summary_id=id).aggregate(total_cash_amount=Sum('amount'))['total_cash_amount'] or 0
    mis_income_total_bank = MiscellaneousIncome.objects.filter(mode_of_transaction=bank_transaction_mode, daily_summary_id=id).aggregate(total_bank_amount=Sum('amount'))['total_bank_amount'] or 0
    mis_income_total_card = MiscellaneousIncome.objects.filter(mode_of_transaction=card_transaction_mode, daily_summary_id=id).aggregate(total_card_amount=Sum('amount'))['total_card_amount'] or 0
    total_mis_income_amount = msc_income.aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    purchase_total_cheque = Purchase.objects.filter(mode_of_transaction=cheque_transaction_mode, daily_summary_id=id).aggregate(total_cheque_amount=Sum('invoice_amount'))['total_cheque_amount'] or 0
    purchase_total_cash = Purchase.objects.filter(mode_of_transaction=cash_transaction_mode, daily_summary_id=id).aggregate(total_cash_amount=Sum('invoice_amount'))['total_cash_amount'] or 0
    purchase_total_bank = Purchase.objects.filter(mode_of_transaction=bank_transaction_mode, daily_summary_id=id).aggregate(total_bank_amount=Sum('invoice_amount'))['total_bank_amount'] or 0
    purchase_total_card = Purchase.objects.filter(mode_of_transaction=card_transaction_mode, daily_summary_id=id).aggregate(total_card_amount=Sum('invoice_amount'))['total_card_amount'] or 0
    purchase_total_credit = Purchase.objects.filter(mode_of_transaction=credit_transaction_mode, daily_summary_id=id).aggregate(total_credit_amount=Sum('invoice_amount'))['total_credit_amount'] or 0
    total_purchase_amount = purchases.aggregate(total_amount=Sum('invoice_amount'))['total_amount'] or 0

    supplier_payment_total_cheque = SupplierPayments.objects.filter(mode_of_transaction=cheque_transaction_mode, daily_summary_id=id).aggregate(total_cheque_amount=Sum('amount'))['total_cheque_amount'] or 0
    supplier_payment_total_cash = SupplierPayments.objects.filter(mode_of_transaction=cash_transaction_mode, daily_summary_id=id).aggregate(total_cash_amount=Sum('amount'))['total_cash_amount'] or 0
    supplier_payment_total_bank = SupplierPayments.objects.filter(mode_of_transaction=bank_transaction_mode, daily_summary_id=id).aggregate(total_bank_amount=Sum('amount'))['total_bank_amount'] or 0
    supplier_payment_total_card = SupplierPayments.objects.filter(mode_of_transaction=card_transaction_mode, daily_summary_id=id).aggregate(total_card_amount=Sum('amount'))['total_card_amount'] or 0
    total_supplier_payment_amount = supplier_payments.aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    expense_total_cheque = Expense.objects.filter(mode_of_transaction=cheque_transaction_mode, daily_summary_id=id).aggregate(total_cheque_amount=Sum('amount'))['total_cheque_amount'] or 0
    expense_total_cash = Expense.objects.filter(mode_of_transaction=cash_transaction_mode, daily_summary_id=id).aggregate(total_cash_amount=Sum('amount'))['total_cash_amount'] or 0
    expense_total_bank = Expense.objects.filter(mode_of_transaction=bank_transaction_mode, daily_summary_id=id).aggregate(total_bank_amount=Sum('amount'))['total_bank_amount'] or 0
    expense_total_card = Expense.objects.filter(mode_of_transaction=card_transaction_mode, daily_summary_id=id).aggregate(total_card_amount=Sum('amount'))['total_card_amount'] or 0
    total_expense_amount = expense.aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    bank_deposit_total_cheque = BankDeposits.objects.filter(mode_of_transaction=cheque_transaction_mode, daily_summary_id=id).aggregate(total_cheque_amount=Sum('amount'))['total_cheque_amount'] or 0
    bank_deposit_total_cash = BankDeposits.objects.filter(mode_of_transaction=cash_transaction_mode, daily_summary_id=id).aggregate(total_cash_amount=Sum('amount'))['total_cash_amount'] or 0
    bank_deposit_total_bank = BankDeposits.objects.filter(mode_of_transaction=bank_transaction_mode, daily_summary_id=id).aggregate(total_bank_amount=Sum('amount'))['total_bank_amount'] or 0
    bank_deposit_total_card = BankDeposits.objects.filter(mode_of_transaction=card_transaction_mode, daily_summary_id=id).aggregate(total_card_amount=Sum('amount'))['total_card_amount'] or 0
    bank_deposit_amount = bank_deposit.aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    withdrawal_total_cheque = Withdrawal.objects.filter(mode_of_transaction=cheque_transaction_mode, daily_summary_id = id).aggregate(total_cheque_amount=Sum('amount'))['total_cheque_amount'] or 0
    withdrawal_total_cash = Withdrawal.objects.filter(mode_of_transaction=cash_transaction_mode, daily_summary_id = id).aggregate(total_cash_amount=Sum('amount'))['total_cash_amount'] or 0
    total_withdrawal_amount = withdrawal.aggregate(total_amount=Sum('amount'))['total_amount'] or 0   


    # daily_summary_today = DailySummary.objects.get(business_profile=business_profile.id, status='ongoing',daily_summary_id = id, date=today)
    # print('daily_summary_today', list(daily_summary_today.__dict__.values()))

    # if daily_summary_today:
    #     closing_balance = (
    #                 (Decimal(bankdata) + daily_summary_today.sales + daily_summary_today.bank_deposit +
    #                 daily_summary_today.credit_collection + daily_summary_today.miscellaneous_income) -
    #                 (daily_summary_today.purchase + daily_summary_today.supplier_payment + daily_summary_today.expense)
    #             )
    # else:
    closing_balance = bankdata or 0
    return render(request, 'edit_daily_summary.html', {
        'business_profile': business_profile.id,
        'today': today,

        'start_time': business_timing.business_start_time,
        'end_time': business_timing.business_end_time,

        'form': form,
        'bank_sale_form': bank_sale_form,
        'credit_collection_form': credit_collection_form,
        'msc_income_form': msc_income_form,
        'purchase_form': purchase_form,
        'supplier_payments_form': supplier_payments_form,
        'bank_deposit_form': bank_deposit_form,
        'expense_form': expense_form,
        'withdrawal_form':withdrawal_form,

        'msc_income': msc_income,
        'credit_collections': credit_collections,
        'bank_sales': bank_sales,
        'expense_type': expense_type,
        'receipt_type': receipt_type,
        'purchases': purchases,
        'supplier_payments': supplier_payments,
        'bank_deposits': bank_deposit,
        'expenses': expense,
        'withdrawal': withdrawal,

        'cash_on_hand': bankdata,
        'closing_balance': closing_balance,

        'bank_sale_total_cheque_sale': bank_sale_total_cheque_sales,
        'bank_sale_total_card_sale': bank_sale_total_card_sales,
        'bank_sale_total_cash_sale': bank_sale_total_cash_sales,
        'bank_sale_total_credit_sale': bank_sale_total_credit_sales,
        'bank_sale_total_bank_sale': bank_sale_total_bank_sales,
        'total_bank_sale_amount': total_bank_sale_amount,

        'credit_sale_total_cheque_sale': credit_sale_total_cheque_sales,
        'credit_sale_total_cash_sale': credit_sale_total_cash_sales,
        'credit_sale_total_bank_sale': credit_sale_total_bank_sales,
        'credit_sale_total_card_sale': credit_sale_total_card_sales,
        'total_credit_sale_amount': total_credit_sale_amount,

        'mis_income_total_cheque': mis_income_total_cheque,
        'mis_income_total_cash': mis_income_total_cash,
        'mis_income_total_bank': mis_income_total_bank,
        'mis_income_total_card': mis_income_total_card,
        'total_mis_income_amount': total_mis_income_amount,

        'purchase_total_cheque': purchase_total_cheque,
        'purchase_total_cash': purchase_total_cash,
        'purchase_total_bank': purchase_total_bank,
        'purchase_total_credit': purchase_total_credit,
        'purchase_total_card': purchase_total_card,
        'total_purchase_amount': total_purchase_amount,

        'supplier_payment_total_cheque': supplier_payment_total_cheque,
        'supplier_payment_total_cash': supplier_payment_total_cash,
        'supplier_payment_total_bank': supplier_payment_total_bank,
        'supplier_payment_total_card': supplier_payment_total_card,
        'total_supplier_payment_amount': total_supplier_payment_amount,

        'expense_total_cheque': expense_total_cheque,
        'expense_total_cash': expense_total_cash,
        'expense_total_bank': expense_total_bank,
        'expense_total_card': expense_total_card,
        'total_expense_amount': total_expense_amount,

        'bank_deposit_total_cheque': bank_deposit_total_cheque,
        'bank_deposit_total_cash': bank_deposit_total_cash,
        'bank_deposit_total_bank': bank_deposit_total_bank,
        'bank_deposit_total_card': bank_deposit_total_card,
        'bank_deposit_amount': bank_deposit_amount,

        'withdrawal_total_cheque':withdrawal_total_cheque,
        'withdrawal_total_cash':withdrawal_total_cash,
        'total_withdrawal_amount':total_withdrawal_amount,


        'id': id
    })

from datetime import date, datetime, timedelta
from django.db.models import Max

def get_supplier_outstanding(request,id):
    try:
        supplier_obj = Supplier.objects.get(id=id)
        outstanding_amount = supplier_obj.outstanding
    except Supplier.DoesNotExist:   
        outstanding_amount = 0 
    return JsonResponse({'outstanding_amount': outstanding_amount})

def get_customer_outstanding(request, id):
    try:
        customer_obj = Customer.objects.get(id=id)
        outstanding_amount = customer_obj.outstanding
    except Customer.DoesNotExist:
        outstanding_amount = 0
    return JsonResponse({'outstanding_amount': outstanding_amount})

def create_daily_summary(request):
    id = request.GET.get('id')
    today = date.today()
    yesterday = datetime.now() - timedelta(days=1)
    yesterday_date = yesterday.date()
    shop_admin = get_object_or_404(ShopAdmin, user=request.user)
    shop = shop_admin.shop
    # Retrieve the business profile associated with the shop
    business_profile = get_object_or_404(BusinessProfile, name=shop.name)
    cheque_transaction_mode = None
    cash_transaction_mode = None
    bank_transaction_mode = None
    credit_transaction_mode = None
    card_transaction_mode = None

    
    try:
        cheque_transaction_mode = TransactionMode.objects.get(name="cheque")
    except TransactionMode.DoesNotExist:
        pass 
    try:
        cash_transaction_mode = TransactionMode.objects.get(name="cash")
    except TransactionMode.DoesNotExist:
        pass 
    try:
        bank_transaction_mode = TransactionMode.objects.get(name="bank transfer")
    except TransactionMode.DoesNotExist:
        pass 
    try:
        credit_transaction_mode = TransactionMode.objects.get(name="credit")
    except TransactionMode.DoesNotExist:
        pass 
    try:
        card_transaction_mode = TransactionMode.objects.get(name="card")
    except TransactionMode.DoesNotExist:
        pass 
    if BusinessTiming.objects.filter(business_profile=business_profile.id).exists():
        business_timing = BusinessTiming.objects.filter(business_profile=business_profile.id).first()
    else:
        messages.warning(request, "Create business timing first.")
        return redirect('create_business_timing')
    # business_timing = BusinessTiming.objects.filter(business_profile=business_profile.id).first()
    if request.method == 'POST':
        form = DailySummaryForm(request.POST)
        if form.is_valid():
            if DailySummary.objects.filter(daily_summary_id=id).exists():
                return redirect('daily_summary_list')  # Redirect if it already exists
            else:
                instance = form.save(commit=False)

                # bank_transfer_sales = BankSales.objects.filter(
                #     business_profile=business_profile.id, 
                #     daily_summary_id=id,
                #     mode_of_transaction__name="bank transfer"
                # ).aggregate(total_amount=Sum('amount'))['total_amount'] or 0

                # card_sales = BankSales.objects.filter(
                #     business_profile=business_profile.id,
                #     daily_summary_id=id,
                #     mode_of_transaction__name="card"
                # ).aggregate(total_amount=Sum('amount'))['total_amount'] or 0

                # cheque_sales = BankSales.objects.filter(
                #     business_profile=business_profile.id,
                #     daily_summary_id=id,
                #     mode_of_transaction__name="cheque"
                # ).aggregate(total_amount=Sum('amount'))['total_amount'] or 0

                # # Calculate the total bank deposit amount
                # instance.bank_deposit += bank_transfer_sales + card_sales + cheque_sales

                # instance.sales = instance.cash_sale + instance.credit_sale
                # instance.closing_balance = (
                #     (instance.opening_balance + instance.sales + instance.bank_deposit
                #     + instance.credit_collection
                #     + instance.miscellaneous_income)-
                #     ( instance.purchase
                #     + instance.supplier_payment
                #     + instance.expense)
                    
                # )
                msc_income = MiscellaneousIncome.objects.filter(business_profile=business_profile.id, daily_summary_id = id)
                purchases = Purchase.objects.filter(business_profile=business_profile.id, daily_summary_id = id)
                supplier_payments = SupplierPayments.objects.filter(business_profile=business_profile.id, daily_summary_id = id)
                expense = Expense.objects.filter(business_profile=business_profile.id, daily_summary_id = id)
                bank_sales = BankSales.objects.filter(business_profile=business_profile.id, daily_summary_id = id)
                credit_collections = CreditCollection.objects.filter(business_profile=business_profile.id, daily_summary_id = id)

                withdrawal = Withdrawal.objects.filter(business_profile=business_profile.id, daily_summary_id = id)
                withdrawal_total = withdrawal.aggregate(total_amount=Sum('amount'))['total_amount'] or 0

                total_bank_sale_amount = bank_sales.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
                bank_sale_total_credit_sales = BankSales.objects.filter(mode_of_transaction=credit_transaction_mode, daily_summary_id = id).aggregate(total_credit_amount=Sum('amount'))['total_credit_amount'] or 0


                # instance.daily_summary_id = id

                bank_sale_total_cheque_sales = BankSales.objects.filter(mode_of_transaction=cheque_transaction_mode, daily_summary_id = id).aggregate(total_cheque_amount=Sum('amount'))['total_cheque_amount'] or 0
                total_bank_sale_amount = bank_sales.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
                total_credit_sale_amount = credit_collections.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
                total_mis_income_amount = msc_income.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
                total_cash_sale = (total_bank_sale_amount  - bank_sale_total_credit_sales)

                purchase_total_cash = Purchase.objects.filter(mode_of_transaction=cash_transaction_mode, daily_summary_id = id).aggregate(total_cash_amount=Sum('invoice_amount'))['total_cash_amount'] or 0
                supplier_payment_total_cash = SupplierPayments.objects.filter(mode_of_transaction=cash_transaction_mode, daily_summary_id = id).aggregate(total_cash_amount=Sum('amount'))['total_cash_amount'] or 0
                expense_total_cash = Expense.objects.filter(mode_of_transaction=cash_transaction_mode, daily_summary_id = id).aggregate(total_cash_amount=Sum('amount'))['total_cash_amount'] or 0

                bank_deposit_total_cheque = BankDeposits.objects.filter(mode_of_transaction=cheque_transaction_mode, daily_summary_id = id).aggregate(total_cheque_amount=Sum('amount'))['total_cheque_amount'] or 0
                bank_deposit_total_cash = BankDeposits.objects.filter(mode_of_transaction=cash_transaction_mode, daily_summary_id = id).aggregate(total_cash_amount=Sum('amount'))['total_cash_amount'] or 0
                bank_deposit_total_bank = BankDeposits.objects.filter(mode_of_transaction=bank_transaction_mode, daily_summary_id = id).aggregate(total_bank_amount=Sum('amount'))['total_bank_amount'] or 0
                bank_deposit_total_card = BankDeposits.objects.filter(mode_of_transaction=card_transaction_mode, daily_summary_id = id).aggregate(total_card_amount=Sum('amount'))['total_card_amount'] or 0



                net_collection = total_cash_sale + total_credit_sale_amount + total_mis_income_amount + withdrawal_total
                net_payment = purchase_total_cash + supplier_payment_total_cash + expense_total_cash
                bank_deposit_collection = bank_deposit_total_cash + bank_deposit_total_bank + bank_deposit_total_cheque + bank_deposit_total_card
                print('net_collection',net_collection)
                print('net_payment',net_payment)
                print('bank_deposit_collection',bank_deposit_collection)
                print('withdrawal_total',withdrawal_total)

                print('opening_balance',instance.opening_balance)
                closing_balance = instance.opening_balance + net_collection - net_payment - bank_deposit_collection
                print('closing_balance',closing_balance)
                instance.closing_balance = closing_balance

                instance.save()
                status = request.POST.get('status')
                if status == "ongoing":
                    return redirect(reverse('save_after_submit') + f'?id={instance.daily_summary_id}')
                return redirect('daily_summary_list')
            # instance = form.save(commit=False)
            # instance.daily_summary_id = id  # Assign the value here
            # instance.save()
            # if instance.status == "ongoing":
            #     return redirect(reverse('create_daily_summary') + f'?id={instance.daily_summary_id}')
            # return redirect('daily_summary_list')
    else:
        form = DailySummaryForm()
        bank_sale_form = BankSaleForm()
        credit_collection_form = CreditCollectionForm()
        msc_income_form = MiscellaneousIncomeForm()
        purchase_form = PurchaseForm()
        supplier_payments_form = SupplierPaymentForm()
        bank_deposit_form = BankDepositsForm()
        expense_form = ExpenseForm()
        withdrawal_form = WithdrawalForm()

    # try:
    #     # Get the latest DailySummary by sorting by date in descending order and taking the first one
    #     # daily_summary = DailySummary.objects.get(date=yesterday_date, business_profile=business_profile.id, daily_summary_id = id)
    #     daily_summary = DailySummary.objects.filter(business_profile=business_profile.id).order_by('-created_on').first()

    #     print('bankdata submit', daily_summary)
    #     bankdata = daily_summary.closing_balance or 0
        
    # except DailySummary.DoesNotExist:
    #     # If no DailySummary exists at all, get the opening balance from BusinessProfile
    #     bankdata = business_profile.opening_balance or 0
    # if DailySummary.objects.exists():
    if DailySummary.objects.filter(business_profile = business_profile.id).exclude(date = today).exists():
        last_daily_summary = DailySummary.objects.filter(business_profile=business_profile.id).exclude(date=today).order_by('-date').first()
        print('last_daily_summary', last_daily_summary)
        # if last_daily_summary is not None:
        #     bankdata = last_daily_summary.closing_balance
        # else:
        #     pass
            # Handle case where no daily summary exists
            # bankdata = None  # Or set to a default value or handle differently

        bankdata = last_daily_summary.closing_balance
    else:
        last_daily_summary = business_profile.opening_balance
        bankdata = last_daily_summary

    # daily_summary = DailySummary.objects.filter(business_profile=business_profile.id)

    # bankdata = business_profile.opening_balance
    # print('today', today)
       
    # closing_balance = daily_summary_today.closing_balance
    # Query for bank sales created on the current date
    bank_sales = BankSales.objects.filter(business_profile=business_profile.id, daily_summary_id = id)
    credit_collections = CreditCollection.objects.filter(business_profile=business_profile.id, daily_summary_id = id)
    msc_income = MiscellaneousIncome.objects.filter(business_profile=business_profile.id, daily_summary_id = id)
    purchases = Purchase.objects.filter(business_profile=business_profile.id, daily_summary_id = id)
    supplier_payments = SupplierPayments.objects.filter(business_profile=business_profile.id, daily_summary_id = id)
    expense = Expense.objects.filter(business_profile=business_profile.id, daily_summary_id = id)
    bank_deposit = BankDeposits.objects.filter(business_profile=business_profile.id, daily_summary_id = id)
    withdrawal = Withdrawal.objects.filter(business_profile=business_profile.id, daily_summary_id = id)

    expense_type = ExpenseType.objects.filter(business_profile=business_profile.id)
    receipt_type = ReceiptType.objects.filter(business_profile=business_profile.id)




    # bank_sale
    bank_sale_total_cheque_sales = BankSales.objects.filter(mode_of_transaction=cheque_transaction_mode, daily_summary_id = id).aggregate(total_cheque_amount=Sum('amount'))['total_cheque_amount'] or 0
    bank_sale_total_cash_sales = BankSales.objects.filter(mode_of_transaction=cash_transaction_mode, daily_summary_id = id).aggregate(total_cash_amount=Sum('amount'))['total_cash_amount'] or 0
    bank_sale_total_credit_sales = BankSales.objects.filter(mode_of_transaction=credit_transaction_mode, daily_summary_id = id).aggregate(total_credit_amount=Sum('amount'))['total_credit_amount'] or 0
    bank_sale_total_card_sales = BankSales.objects.filter(mode_of_transaction=card_transaction_mode, daily_summary_id = id).aggregate(total_card_amount=Sum('amount'))['total_card_amount'] or 0
    bank_sale_total_bank_sales = BankSales.objects.filter(mode_of_transaction=bank_transaction_mode, daily_summary_id = id).aggregate(total_bank_amount=Sum('amount'))['total_bank_amount'] or 0
    total_bank_sale_amount = bank_sales.aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    # credit_sale
    credit_sale_total_cheque_sales = CreditCollection.objects.filter(payment_mode=cheque_transaction_mode, daily_summary_id = id).aggregate(total_cheque_amount=Sum('amount'))['total_cheque_amount'] or 0
    credit_sale_total_cash_sales = CreditCollection.objects.filter(payment_mode=cash_transaction_mode, daily_summary_id = id).aggregate(total_cash_amount=Sum('amount'))['total_cash_amount'] or 0
    credit_sale_total_bank_sales = CreditCollection.objects.filter(payment_mode=bank_transaction_mode, daily_summary_id = id).aggregate(total_bank_amount=Sum('amount'))['total_bank_amount'] or 0
    credit_sale_total_card_sales = CreditCollection.objects.filter(payment_mode=card_transaction_mode, daily_summary_id = id).aggregate(total_card_amount=Sum('amount'))['total_card_amount'] or 0
    total_credit_sale_amount = credit_collections.aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    # mis_income
    mis_income_total_cheque = MiscellaneousIncome.objects.filter(mode_of_transaction=cheque_transaction_mode, daily_summary_id = id).aggregate(total_cheque_amount=Sum('amount'))['total_cheque_amount'] or 0
    mis_income_total_cash = MiscellaneousIncome.objects.filter(mode_of_transaction=cash_transaction_mode, daily_summary_id = id).aggregate(total_cash_amount=Sum('amount'))['total_cash_amount'] or 0
    mis_income_total_bank = MiscellaneousIncome.objects.filter(mode_of_transaction=bank_transaction_mode, daily_summary_id = id).aggregate(total_bank_amount=Sum('amount'))['total_bank_amount'] or 0
    mis_income_total_card = MiscellaneousIncome.objects.filter(mode_of_transaction=card_transaction_mode, daily_summary_id = id).aggregate(total_card_amount=Sum('amount'))['total_card_amount'] or 0
    total_mis_income_amount = msc_income.aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    purchase_total_cheque = Purchase.objects.filter(mode_of_transaction=cheque_transaction_mode, daily_summary_id = id).aggregate(total_cheque_amount=Sum('invoice_amount'))['total_cheque_amount'] or 0
    purchase_total_cash = Purchase.objects.filter(mode_of_transaction=cash_transaction_mode, daily_summary_id = id).aggregate(total_cash_amount=Sum('invoice_amount'))['total_cash_amount'] or 0
    purchase_total_bank = Purchase.objects.filter(mode_of_transaction=bank_transaction_mode, daily_summary_id = id).aggregate(total_bank_amount=Sum('invoice_amount'))['total_bank_amount'] or 0
    purchase_total_card = Purchase.objects.filter(mode_of_transaction=card_transaction_mode, daily_summary_id = id).aggregate(total_card_amount=Sum('invoice_amount'))['total_card_amount'] or 0
    purchase_total_credit = Purchase.objects.filter(mode_of_transaction=credit_transaction_mode, daily_summary_id = id).aggregate(total_credit_amount=Sum('invoice_amount'))['total_credit_amount'] or 0
    total_purchase_amount = purchases.aggregate(total_amount=Sum('invoice_amount'))['total_amount'] or 0

    supplier_payment_total_cheque = SupplierPayments.objects.filter(mode_of_transaction=cheque_transaction_mode, daily_summary_id = id).aggregate(total_cheque_amount=Sum('amount'))['total_cheque_amount'] or 0
    supplier_payment_total_cash = SupplierPayments.objects.filter(mode_of_transaction=cash_transaction_mode, daily_summary_id = id).aggregate(total_cash_amount=Sum('amount'))['total_cash_amount'] or 0
    supplier_payment_total_bank = SupplierPayments.objects.filter(mode_of_transaction=bank_transaction_mode, daily_summary_id = id).aggregate(total_bank_amount=Sum('amount'))['total_bank_amount'] or 0
    supplier_payment_total_card = SupplierPayments.objects.filter(mode_of_transaction=card_transaction_mode, daily_summary_id = id).aggregate(total_card_amount=Sum('amount'))['total_card_amount'] or 0
    total_supplier_payment_amount = supplier_payments.aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    expense_total_cheque = Expense.objects.filter(mode_of_transaction=cheque_transaction_mode, daily_summary_id = id).aggregate(total_cheque_amount=Sum('amount'))['total_cheque_amount'] or 0
    expense_total_cash = Expense.objects.filter(mode_of_transaction=cash_transaction_mode, daily_summary_id = id).aggregate(total_cash_amount=Sum('amount'))['total_cash_amount'] or 0
    expense_total_bank = Expense.objects.filter(mode_of_transaction=bank_transaction_mode, daily_summary_id = id).aggregate(total_bank_amount=Sum('amount'))['total_bank_amount'] or 0
    expense_total_card = Expense.objects.filter(mode_of_transaction=card_transaction_mode, daily_summary_id = id).aggregate(total_card_amount=Sum('amount'))['total_card_amount'] or 0
    total_expense_amount = expense.aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    bank_deposit_total_cheque = BankDeposits.objects.filter(mode_of_transaction=cheque_transaction_mode, daily_summary_id = id).aggregate(total_cheque_amount=Sum('amount'))['total_cheque_amount'] or 0
    bank_deposit_total_cash = BankDeposits.objects.filter(mode_of_transaction=cash_transaction_mode, daily_summary_id = id).aggregate(total_cash_amount=Sum('amount'))['total_cash_amount'] or 0
    bank_deposit_total_bank = BankDeposits.objects.filter(mode_of_transaction=bank_transaction_mode, daily_summary_id = id).aggregate(total_bank_amount=Sum('amount'))['total_bank_amount'] or 0
    bank_deposit_total_card = BankDeposits.objects.filter(mode_of_transaction=card_transaction_mode, daily_summary_id = id).aggregate(total_card_amount=Sum('amount'))['total_card_amount'] or 0
    bank_deposit_amount = bank_deposit.aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    withdrawal_total_cheque = Withdrawal.objects.filter(mode_of_transaction=cheque_transaction_mode, daily_summary_id = id).aggregate(total_cheque_amount=Sum('amount'))['total_cheque_amount'] or 0
    withdrawal_total_cash = Withdrawal.objects.filter(mode_of_transaction=cash_transaction_mode, daily_summary_id = id).aggregate(total_cash_amount=Sum('amount'))['total_cash_amount'] or 0
    total_withdrawal_amount = withdrawal.aggregate(total_amount=Sum('amount'))['total_amount'] or 0   

    # daily_summary_today = DailySummary.objects.get(business_profile=business_profile.id, status='ongoing',daily_summary_id = id, date=today)
    # daily_summary_today = DailySummary.objects.filter(business_profile=business_profile.id, status='ongoing')

    # print('daily_summary_today', daily_summary_today)
    # print(daily_summary_today.bank_deposit)
    # if daily_summary_today:
    #     closing_balance = (
    #                 (bankdata + daily_summary_today.sales + daily_summary_today.bank_deposit +
    #                 daily_summary_today.credit_collection + daily_summary_today.miscellaneous_income) -
    #                 (daily_summary_today.purchase + daily_summary_today.supplier_payment + daily_summary_today.expense)
    #             )
    # else:
    closing_balance = bankdata or 0

    return render(request, 'create_daily_summary.html',
        {
            
            'business_profile': business_profile.id,
            'today':today,

            #business timings
            'start_time':business_timing.business_start_time,
            'end_time':business_timing.business_end_time,

            #forms
            'form': form,
            'bank_sale_form': bank_sale_form,
            'credit_collection_form': credit_collection_form,
            'msc_income_form': msc_income_form,
            'purchase_form':purchase_form,
            'supplier_payments_form':supplier_payments_form,
            'bank_deposit_form':bank_deposit_form,
            'expense_form':expense_form,
            'withdrawal_form':withdrawal_form,
            
            #listings
            'msc_income': msc_income,
            'credit_collections':credit_collections,
            'bank_sales': bank_sales,
            'expense_type':expense_type,
            'receipt_type':receipt_type,
            'purchases':purchases,
            'supplier_payments':supplier_payments,
            'bank_deposits':bank_deposit,
            'expenses':expense,
            'withdrawal':withdrawal,

            #cash on hand
            'cash_on_hand':bankdata,
            'closing_balance':closing_balance,

            # calculated vales
            'bank_sale_total_cheque_sale':bank_sale_total_cheque_sales,
            'bank_sale_total_card_sale':bank_sale_total_card_sales,
            'bank_sale_total_cash_sale':bank_sale_total_cash_sales,
            'bank_sale_total_credit_sale':bank_sale_total_credit_sales,
            'bank_sale_total_bank_sale':bank_sale_total_bank_sales,
            'total_bank_sale_amount':total_bank_sale_amount,

            'credit_sale_total_cheque_sale':credit_sale_total_cheque_sales,
            'credit_sale_total_cash_sale':credit_sale_total_cash_sales,
            'credit_sale_total_bank_sale':credit_sale_total_bank_sales,
            'credit_sale_total_card_sale':credit_sale_total_card_sales,
            'total_credit_sale_amount':total_credit_sale_amount,

            'mis_income_total_cheque':mis_income_total_cheque,
            'mis_income_total_cash':mis_income_total_cash,
            'mis_income_total_bank':mis_income_total_bank,
            'mis_income_total_card':mis_income_total_card,
            'total_mis_income_amount':total_mis_income_amount,

            'purchase_total_cheque':purchase_total_cheque,
            'purchase_total_cash':purchase_total_cash,
            'purchase_total_bank':purchase_total_bank,
            'purchase_total_credit':purchase_total_credit,
            'purchase_total_card':purchase_total_card,
            'total_purchase_amount':total_purchase_amount,

            'supplier_payment_total_cheque':supplier_payment_total_cheque,
            'supplier_payment_total_cash':supplier_payment_total_cash,
            'supplier_payment_total_bank':supplier_payment_total_bank,
            'supplier_payment_total_card':supplier_payment_total_card,
            'total_supplier_payment_amount':total_supplier_payment_amount,

            'expense_total_cheque':expense_total_cheque,
            'expense_total_cash':expense_total_cash,
            'expense_total_bank':expense_total_bank,
            'expense_total_card':expense_total_card,
            'total_expense_amount':total_expense_amount,

            'bank_deposit_total_cheque':bank_deposit_total_cheque,
            'bank_deposit_total_cash':bank_deposit_total_cash,
            'bank_deposit_total_bank':bank_deposit_total_bank,
            'bank_deposit_total_card':bank_deposit_total_card,
            'bank_deposit_amount':bank_deposit_amount,

            'withdrawal_total_cheque':withdrawal_total_cheque,
            'withdrawal_total_cash':withdrawal_total_cash,
            'total_withdrawal_amount':total_withdrawal_amount,

    
            'id': id


        }
    )





def create_bank_sale(request):
    if request.method == 'POST':
        form = BankSaleForm(request.POST)
        daily_summary_id = request.POST.get('daily_summary_id')  # Get the daily summary ID from the form
        if form.is_valid():
            form = form.save(commit=False)
            daily_summary_id = request.POST.get('daily_summary_id')  # Get the daily summary ID from the form
            form.daily_summary_id = daily_summary_id  # Assign the daily summary ID to the bank sale instance
            # form.save()
            if form.mode_of_transaction.name == 'credit':
                customer = form.customer
                customer.outstanding = customer.outstanding + form.amount
                customer.save()
            form.save()

            # return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}')
            if DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
                return redirect(reverse('save_after_submit') + f'?id={daily_summary_id}#1')
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}#1')
        elif DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
                # Redirect to the edit page if the daily summary already exists
            return redirect(reverse('save_after_submit') + f'?id={daily_summary_id}#1')
        else:
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}#1')


        
            
def list_bank_sales(request):
    # id = request.GET.get('id')
    shop_admin = get_object_or_404(ShopAdmin, user=request.user)
    shop = shop_admin.shop
    
    # Retrieve the business profile associated with the shop
    business_profile = get_object_or_404(BusinessProfile, name=shop.name)
    bank_sales = BankSales.objects.filter(business_profile=business_profile.id)
    # print(bank_sales)
    return render(request, 'create_daily_summary.html', {'bank_sales': bank_sales})

def create_credit_collection(request):
    if request.method == 'POST':
        form = CreditCollectionForm(request.POST)
        daily_summary_id = request.POST.get('daily_summary_id')
        if form.is_valid():
            form = form.save(commit=False)
            daily_summary_id = request.POST.get('daily_summary_id')  # Get the daily summary ID from the form
            form.daily_summary_id = daily_summary_id  # Assign the daily summary ID to the bank sale instance
            # form.save()
            customer = form.customer
            customer.outstanding = customer.outstanding - form.amount
            customer.save()
            form.save()

            # Redirect to the 'create_daily_summary' URL with the dailySummaryId in the query parameters
    #         return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}')
    # return redirect('create_daily_summary')
            if DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
                return redirect(reverse('save_after_submit') + f'?id={daily_summary_id}#2')
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}#2')
        elif DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
                # Redirect to the edit page if the daily summary already exists
            return redirect(reverse('save_after_submit') + f'?id={daily_summary_id}#2')
        else:
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}#2')


def list_credit_collection(request):
    shop_admin = get_object_or_404(ShopAdmin, user=request.user)
    shop = shop_admin.shop
    
    # Retrieve the business profile associated with the shop
    business_profile = get_object_or_404(BusinessProfile, name=shop.name)
    credit_collections = CreditCollection.objects.filter(business_profile=business_profile.id)
    # print(bank_sales)
    return render(request, 'create_daily_summary.html', {'credit_collections': credit_collections})

def create_misc_income(request):
    if request.method == 'POST':
        form = MiscellaneousIncomeForm(request.POST)
        daily_summary_id = request.POST.get('daily_summary_id')
        if form.is_valid():
            form = form.save(commit=False)
            daily_summary_id = request.POST.get('daily_summary_id')  # Get the daily summary ID from the form
            form.daily_summary_id = daily_summary_id  # Assign the daily summary ID to the bank sale instance
            form.save()
            # Redirect to the 'create_daily_summary' URL with the dailySummaryId in the query parameters
    #         return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}')
    # return redirect('create_daily_summary')
            if DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
                return redirect(reverse('save_after_submit') + f'?id={daily_summary_id}#3')
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}#3')
        elif DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
                # Redirect to the edit page if the daily summary already exists
            return redirect(reverse('save_after_submit') + f'?id={daily_summary_id}#3')
        else:
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}#3')


def list_msc_income(request):
    shop_admin = get_object_or_404(ShopAdmin, user=request.user)
    shop = shop_admin.shop
    
    # Retrieve the business profile associated with the shop
    business_profile = get_object_or_404(BusinessProfile, name=shop.name)
    msc_income = MiscellaneousIncome.objects.filter(business_profile=business_profile.id)
    # print(bank_sales)
    return render(request, 'create_daily_summary.html', {'msc_income': msc_income})

def create_purchase(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        daily_summary_id = request.POST.get('daily_summary_id')
        if form.is_valid():
            form = form.save(commit=False)
            daily_summary_id = request.POST.get('daily_summary_id')  # Get the daily summary ID from the form
            form.daily_summary_id = daily_summary_id  # Assign the daily summary ID to the bank sale instance
            # form.save()
            if form.mode_of_transaction.name == 'credit':
                supplier = form.supplier
                supplier.outstanding = supplier.outstanding + form.invoice_amount
                supplier.save()
            form.save()

            # Redirect to the 'create_daily_summary' URL with the dailySummaryId in the query parameters
    #         return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}')
    # return redirect('create_daily_summary')
            if DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
                return redirect(reverse('save_after_submit') + f'?id={daily_summary_id}#5')
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}#5')
        elif DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
                # Redirect to the edit page if the daily summary already exists
            return redirect(reverse('save_after_submit') + f'?id={daily_summary_id}#5')
        else:
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}#5')


def list_purchases(request):
    shop_admin = get_object_or_404(ShopAdmin, user=request.user)
    shop = shop_admin.shop
    
    # Retrieve the business profile associated with the shop
    business_profile = get_object_or_404(BusinessProfile, name=shop.name)
    purchases = Purchase.objects.filter(business_profile=business_profile.id)
    return render(request, 'create_daily_summary.html', {'purchases': purchases})

def create_supplier_payment(request):
    if request.method == 'POST':
        form = SupplierPaymentForm(request.POST)
        daily_summary_id = request.POST.get('daily_summary_id')
        if form.is_valid():
            form = form.save(commit=False)
            daily_summary_id = request.POST.get('daily_summary_id')  # Get the daily summary ID from the form
            form.daily_summary_id = daily_summary_id  # Assign the daily summary ID to the bank sale instance
            # form.save()
            supplier = form.supplier
            supplier.outstanding = supplier.outstanding - form.amount
            supplier.save() 
            form.save()

            # Redirect to the 'create_daily_summary' URL with the dailySummaryId in the query parameters
    #         return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}')
    # return redirect('create_daily_summary')
            if DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
                return redirect(reverse('save_after_submit') + f'?id={daily_summary_id}#6')
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}#6')
        elif DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
                # Redirect to the edit page if the daily summary already exists
            return redirect(reverse('save_after_submit') + f'?id={daily_summary_id}#6')
        else:
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}#6')


def list_supplier_payment(request):
    shop_admin = get_object_or_404(ShopAdmin, user=request.user)
    shop = shop_admin.shop
    
    # Retrieve the business profile associated with the shop
    business_profile = get_object_or_404(BusinessProfile, name=shop.name)
    supplier_payments = SupplierPayments.objects.filter(business_profile=business_profile.id)
    return render(request, 'create_daily_summary.html', {'supplier_payments': supplier_payments})


def create_bank_deposit(request):
    if request.method == 'POST':
        form = BankDepositsForm(request.POST)
        daily_summary_id = request.POST.get('daily_summary_id')
        if form.is_valid():
            form = form.save(commit=False)
            daily_summary_id = request.POST.get('daily_summary_id')  # Get the daily summary ID from the form
            form.daily_summary_id = daily_summary_id  # Assign the daily summary ID to the bank sale instance
            form.save()
    #         return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}')
    # return redirect('create_daily_summary')
            if DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
                return redirect(reverse('save_after_submit') + f'?id={daily_summary_id}#8')
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}#8')
        elif DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
                # Redirect to the edit page if the daily summary already exists
            return redirect(reverse('save_after_submit') + f'?id={daily_summary_id}#8')
        else:
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}#8')


def list_bank_deposit(request):
    shop_admin = get_object_or_404(ShopAdmin, user=request.user)
    shop = shop_admin.shop
    # Retrieve the business profile associated with the shop
    business_profile = get_object_or_404(BusinessProfile, name=shop.name)
    bank_deposit = BankDeposits.objects.filter(business_profile=business_profile.id)
    # print(bank_sales)
    return render(request, 'create_daily_summary.html', {'bank_deposit': bank_deposit})

def create_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        daily_summary_id = request.POST.get('daily_summary_id')
        if form.is_valid():
            form = form.save(commit=False)
            daily_summary_id = request.POST.get('daily_summary_id')  # Get the daily summary ID from the form
            form.daily_summary_id = daily_summary_id  # Assign the daily summary ID to the bank sale instance
            form.save()
    #         return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}')
    # return redirect('create_daily_summary')
            if DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
                return redirect(reverse('save_after_submit') + f'?id={daily_summary_id}#7')
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}#7')
        elif DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
                # Redirect to the edit page if the daily summary already exists
            return redirect(reverse('save_after_submit') + f'?id={daily_summary_id}#7')
        else:
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}#7')


def list_expense(request):
    shop_admin = get_object_or_404(ShopAdmin, user=request.user)
    shop = shop_admin.shop
    
    # Retrieve the business profile associated with the shop
    business_profile = get_object_or_404(BusinessProfile, name=shop.name)
    expense = Expense.objects.filter(business_profile=business_profile.id)
    # print(bank_sales)
    return render(request, 'create_daily_summary.html', {'expenses': expense})

def edit_daily_summary(request, id):
    summary = get_object_or_404(DailySummary, id=id)
    if request.method == 'POST':
        form = DailySummaryForm(request.POST, instance=summary)
        if form.is_valid():
            form.save()
            return redirect('daily_summary_list')
    else:
        form = DailySummaryForm(instance=summary)
    return render(request, 'create_daily_summary.html', {'form': form})

def delete_daily_summary(request, id):
    summary = get_object_or_404(DailySummary, id=id)
    if request.method == 'POST':
        summary.delete()
        return redirect('daily_summary_list')
    return render(request, 'daily_summary_confirm_delete.html', {'summary': summary})


def fetch_cheque_numbers(request):
    shop_admin = get_object_or_404(ShopAdmin, user=request.user)
    shop = shop_admin.shop
    
    # Retrieve the business profile associated with the shop
    business_profile = get_object_or_404(BusinessProfile, name=shop.name)
    cheque_numbers = set()
    
    # Fetch cheque numbers from all specified models
    cheque_numbers.update(BankSales.objects.filter(business_profile=business_profile.id, daily_summary_id = id).values_list('cheque_no', flat=True))

    cheque_numbers.update(CreditCollection.objects.filter(business_profile=business_profile.id, daily_summary_id = id).values_list('cheque_no', flat=True))
    cheque_numbers.update(MiscellaneousIncome.objects.filter(business_profile=business_profile.id, daily_summary_id = id).values_list('cheque_no', flat=True))
    cheque_numbers.update(Purchase.objects.filter(business_profile=business_profile.id, daily_summary_id = id).values_list('cheque_no', flat=True))
    cheque_numbers.update(SupplierPayments.objects.filter(business_profile=business_profile.id, daily_summary_id = id).values_list('cheque_no', flat=True))
    cheque_numbers.update(Expense.objects.filter(business_profile=business_profile.id, daily_summary_id = id).values_list('cheque_no', flat=True))
    print(cheque_numbers)
    cheque_numbers = list(cheque_numbers)
    return JsonResponse(cheque_numbers, safe=False)

def create_withdrawal(request):
    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        daily_summary_id = request.POST.get('daily_summary_id')
        if form.is_valid():
            form = form.save(commit=False)
            daily_summary_id = request.POST.get('daily_summary_id')
            form.daily_summary_id = daily_summary_id
            form.save()
            if DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
                return redirect(reverse('save_after_submit') + f'?id={daily_summary_id}#4')
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}#4')
        elif DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
                # Redirect to the edit page if the daily summary already exists
            return redirect(reverse('save_after_submit') + f'?id={daily_summary_id}#4')
        else:
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}#4')

    #         return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}')
    # return redirect('create_daily_summary')
    # else:
    #     form = WithdrawalForm()
    #     shop_admin = get_object_or_404(ShopAdmin, user=request.user)
    #     shop = shop_admin.shop
    #     business_profile = get_object_or_404(BusinessProfile, name=shop.name)
    #     return render(request, 'withdrawal_form.html', {'form': form, 'business_profile': business_profile.id})

def list_withdrawal(request):
    shop_admin = get_object_or_404(ShopAdmin, user=request.user)
    shop = shop_admin.shop
    business_profile = get_object_or_404(BusinessProfile, name=shop.name)
    withdrawals = Withdrawal.objects.filter(business_profile=business_profile.id)
    return render(request, 'create_daily_summary.html', {'withdrawals': withdrawals, 'business_profile': business_profile.id})

# class WithdrawalListView(View):
#     def get(self, request):
#         shop_admin = get_object_or_404(ShopAdmin, user=request.user)
#         shop = shop_admin.shop
        
#         # Retrieve the business profile associated with the shop
#         business_profile = get_object_or_404(BusinessProfile, name=shop.name)
#         withdrawals = Withdrawal.objects.all()
#         return render(request, 'withdrawal_list.html', {'withdrawals': withdrawals, 'business_profile':business_profile.id})

# class WithdrawalCreateView(View):
#     def get(self, request):
#         shop_admin = get_object_or_404(ShopAdmin, user=request.user)
#         shop = shop_admin.shop
        
#         # Retrieve the business profile associated with the shop
#         business_profile = get_object_or_404(BusinessProfile, name=shop.name)
#         form = WithdrawalForm()
#         return render(request, 'withdrawal_form.html', {'form': form, 'business_profile':business_profile.id})

#     def post(self, request):
#         shop_admin = get_object_or_404(ShopAdmin, user=request.user)
#         shop = shop_admin.shop
        
#         # Retrieve the business profile associated with the shop
#         business_profile = get_object_or_404(BusinessProfile, name=shop.name)
#         form = WithdrawalForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect(reverse('withdrawal_list'))
#         return render(request, 'withdrawal_form.html', {'form': form, 'business_profile':business_profile.id})


def get_daily_summary_data(request,id):
    # id = request.GET.get('id')
    today = date.today()
    shop_admin = get_object_or_404(ShopAdmin, user=request.user)
    shop = shop_admin.shop
    business_profile = get_object_or_404(BusinessProfile, name=shop.name)
    cheque_transaction_mode = None
    cash_transaction_mode = None
    bank_transaction_mode = None
    credit_transaction_mode = None
    card_transaction_mode = None

    
    try:
        cheque_transaction_mode = TransactionMode.objects.get(name="cheque")
    except TransactionMode.DoesNotExist:
        pass 
    try:
        cash_transaction_mode = TransactionMode.objects.get(name="cash")
    except TransactionMode.DoesNotExist:
        pass 
    try:
        bank_transaction_mode = TransactionMode.objects.get(name="bank transfer")
    except TransactionMode.DoesNotExist:
        pass 
    try:
        credit_transaction_mode = TransactionMode.objects.get(name="credit")
    except TransactionMode.DoesNotExist:
        pass 
    try:
        card_transaction_mode = TransactionMode.objects.get(name="card")
    except TransactionMode.DoesNotExist:
        pass 

    msc_income = MiscellaneousIncome.objects.filter(business_profile=business_profile.id, daily_summary_id = id)
    # purchases = Purchase.objects.filter(business_profile=business_profile.id, daily_summary_id = id)
    # supplier_payments = SupplierPayments.objects.filter(business_profile=business_profile.id, daily_summary_id = id)
    # expense = Expense.objects.filter(business_profile=business_profile.id, daily_summary_id = id)

    bank_sales = BankSales.objects.filter(business_profile=business_profile.id, daily_summary_id = id)
    credit_collections = CreditCollection.objects.filter(business_profile=business_profile.id, daily_summary_id = id)

    withdrawal = Withdrawal.objects.filter(business_profile=business_profile.id, daily_summary_id = id)
    withdrawal_total = withdrawal.aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    total_bank_sale_amount = bank_sales.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
    bank_sale_total_credit_sales = BankSales.objects.filter(mode_of_transaction=credit_transaction_mode, daily_summary_id = id).aggregate(total_credit_amount=Sum('amount'))['total_credit_amount'] or 0


    # instance.daily_summary_id = id

    # bank_sale_total_cheque_sales = BankSales.objects.filter(mode_of_transaction=cheque_transaction_mode, daily_summary_id = id).aggregate(total_cheque_amount=Sum('amount'))['total_cheque_amount'] or 0
    total_bank_sale_amount = bank_sales.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
    total_credit_sale_amount = credit_collections.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
    total_mis_income_amount = msc_income.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
    total_cash_sale = (total_bank_sale_amount  - bank_sale_total_credit_sales)

    # net_payment calculation
    purchase_total_cash = Purchase.objects.filter(mode_of_transaction=cash_transaction_mode, daily_summary_id = id).aggregate(total_cash_amount=Sum('invoice_amount'))['total_cash_amount'] or 0
    supplier_payment_total_cash = SupplierPayments.objects.filter(mode_of_transaction=cash_transaction_mode, daily_summary_id = id).aggregate(total_cash_amount=Sum('amount'))['total_cash_amount'] or 0
    expense_total_cash = Expense.objects.filter(mode_of_transaction=cash_transaction_mode, daily_summary_id = id).aggregate(total_cash_amount=Sum('amount'))['total_cash_amount'] or 0

    bank_deposit_total_cheque = BankDeposits.objects.filter(mode_of_transaction=cheque_transaction_mode, daily_summary_id = id).aggregate(total_cheque_amount=Sum('amount'))['total_cheque_amount'] or 0
    bank_deposit_total_cash = BankDeposits.objects.filter(mode_of_transaction=cash_transaction_mode, daily_summary_id = id).aggregate(total_cash_amount=Sum('amount'))['total_cash_amount'] or 0
    bank_deposit_total_bank = BankDeposits.objects.filter(mode_of_transaction=bank_transaction_mode, daily_summary_id = id).aggregate(total_bank_amount=Sum('amount'))['total_bank_amount'] or 0
    bank_deposit_total_card = BankDeposits.objects.filter(mode_of_transaction=card_transaction_mode, daily_summary_id = id).aggregate(total_card_amount=Sum('amount'))['total_card_amount'] or 0



    net_collection = total_cash_sale + total_credit_sale_amount + total_mis_income_amount + withdrawal_total
    net_payment = purchase_total_cash + supplier_payment_total_cash + expense_total_cash
    bank_deposit_collection = bank_deposit_total_cash + bank_deposit_total_bank + bank_deposit_total_cheque + bank_deposit_total_card

    print('net_collection',net_collection)
    print('net_payment',net_payment)
    print('bank_deposit_collection',bank_deposit_collection)
    print('withdrawal_total',withdrawal_total)

    # if DailySummary.objects.exists():
    if DailySummary.objects.filter(business_profile = business_profile.id).exclude(date = today).exists():
        # last_daily_summary = DailySummary.objects.filter(business_profile=business_profile.id).exclude(date=today).order_by('-date').first()
        last_daily_summary = DailySummary.objects.filter(business_profile=business_profile.id).exclude(date=today).order_by('-date').first()
        last_daily_summary_data = last_daily_summary.closing_balance
    else:
        last_daily_summary = business_profile.opening_balance
        last_daily_summary_data = last_daily_summary
    

    closing_balance = Decimal(last_daily_summary_data) + net_collection - net_payment - bank_deposit_collection
    # print('closing_balance',closing_balance)
    return JsonResponse({'closing_balance':closing_balance}, safe=False)


def create_all_banks(request):
    try:
        for bank_name in BANK_CHOICES:
            AllBank.objects.get_or_create(name=bank_name[0])
        messages.success(request, 'All banks created successfully')
        return redirect('bank_list')
    except Exception as e:
        messages.error(request, 'Failed to create banks')
        return redirect('bank_list')


class DailyCollectionReportView(View):
    def get(self, request):
        return render(request, 'daily_collection_report.html')


class SalesReportView(View):
    def get(self, request):
        return render(request, 'sales_report.html')


class PurchaseReportView(View):
    def get(self, request):
        return render(request, 'purchase_report.html')


class MscIncomeReportView(View):
    def get(self, request):
        return render(request, 'msc_income_report.html')

class SupplierPaymentReportView(View):
    def get(self, request):
        shop_admin = get_object_or_404(ShopAdmin, user=request.user)
        shop = shop_admin.shop
        business_profile = get_object_or_404(BusinessProfile, name=shop.name)
        suppliers = Supplier.objects.filter(business_profile=business_profile.id)
        print('sup',suppliers)
        return render(request, 'supplier_payment_report.html',{'suppliers': suppliers, 'business_profile': business_profile.id} )


class BankStatementView(View):
    def get(self, request):
        shop_admin = get_object_or_404(ShopAdmin, user=request.user)
        shop = shop_admin.shop
        business_profile = get_object_or_404(BusinessProfile, name=shop.name)
        
        banks = Bank.objects.filter(business_profile=business_profile.id)
        return render(request, 'bank_statement.html', {'banks': banks})


def edit_bank_sale(request, pk):
    bank_sale = get_object_or_404(BankSales, pk=pk)
    daily_summary_id = bank_sale.daily_summary_id
    if request.method == 'POST':
        form = BankSaleForm(request.POST, request.FILES, instance=bank_sale)    
        if form.is_valid():
            form.save()
            if DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
                return redirect(reverse('save_after_submit') + f'?id={daily_summary_id}#1')
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}#1')
        elif DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
            return redirect(reverse('save_after_submit') + f'?id={daily_summary_id}#1')
        else:
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}#1')
    else:
        form = BankSaleForm(instance=bank_sale)
    return render(request, 'edit_bank_sale.html', {'form': form, 'bank_sale': bank_sale})

def edit_credit_collection(request, pk):
    credit_instance = get_object_or_404(CreditCollection, pk=pk)
    daily_summary_id = credit_instance.daily_summary_id
    if request.method == 'POST':
        form = CreditCollectionForm(request.POST, request.FILES, instance=credit_instance)    
        if form.is_valid():
            form.save()
            if DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
                return redirect(reverse('save_after_submit') + f'?id={daily_summary_id}#2')
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}#2')
        elif DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
            return redirect(reverse('save_after_submit') + f'?id={daily_summary_id}#2')
        else:
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}#2')
    else:
        form = CreditCollectionForm(instance=credit_instance)
    return render(request, 'edit_credit_collection.html', {'form': form, 'credit_instance': credit_instance})


def edit_miscellaneous_income(request, pk):
    misc_instance = get_object_or_404(MiscellaneousIncome, pk=pk)
    daily_summary_id = misc_instance.daily_summary_id
    if request.method == 'POST':
        form = MiscellaneousIncomeForm(request.POST, request.FILES, instance=misc_instance)    
        if form.is_valid():
            form.save()
            if DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
                return redirect(reverse('save_after_submit') + f'?id={daily_summary_id}#3')
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}#3')
        elif DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
            return redirect(reverse('save_after_submit') + f'?id={daily_summary_id}#3')
        else:
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}#3')
    else:
        form = MiscellaneousIncomeForm(instance=misc_instance)
    return render(request, 'edit_miscellaneous_income.html', {'form': form, 'misc_instance': misc_instance})

def edit_withdrawal(request, pk):
    withdrawal_instance = get_object_or_404(Withdrawal, pk=pk)
    daily_summary_id = withdrawal_instance.daily_summary_id
    if request.method == 'POST':
        form = WithdrawalForm(request.POST, request.FILES, instance=withdrawal_instance)    
        if form.is_valid():
            form.save()
            if DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
                return redirect(reverse('save_after_submit') + f'?id={daily_summary_id}#4')
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}#4')
        elif DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
            return redirect(reverse('save_after_submit') + f'?id={daily_summary_id}#4')
        else:
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}#4')
    else:
        form = WithdrawalForm(instance=withdrawal_instance)
    return render(request, 'edit_withdrawal.html', {'form': form, 'withdrawal_instance': withdrawal_instance})

def edit_purchase(request, pk):
    purchase_instance = get_object_or_404(Purchase, pk=pk)
    daily_summary_id = purchase_instance.daily_summary_id
    if request.method == 'POST':
        form = PurchaseForm(request.POST, request.FILES, instance=purchase_instance)
        if form.is_valid():
            form.save()
            if DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
                return redirect(reverse('save_after_submit') + f'?id={daily_summary_id}#5')
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}#5')
        elif DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
            return redirect(reverse('save_after_submit') + f'?id={daily_summary_id}#5')
        else:
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}#5')
    else:
        form = PurchaseForm(instance=purchase_instance)
    return render(request, 'edit_purchase.html', {'form': form, 'purchase_instance': purchase_instance})


def edit_supplier_payment(request, pk):
    supplier_instance = get_object_or_404(SupplierPayments, pk=pk)
    daily_summary_id = supplier_instance.daily_summary_id
    if request.method == 'POST':
        form = SupplierPaymentForm(request.POST, request.FILES, instance=supplier_instance)
        if form.is_valid():
            form.save()
            if DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
                return redirect(reverse('save_after_submit') + f'?id={daily_summary_id}#6')
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}#6')
        elif DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
            return redirect(reverse('save_after_submit') + f'?id={daily_summary_id}#6')
        else:
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}#6')
    else:
        form = SupplierPaymentForm(instance=supplier_instance)
    return render(request, 'edit_supplier_payment.html', {'form': form, 'supplier_instance': supplier_instance})

def edit_expense(request, pk):
    expense_instance = get_object_or_404(Expense, pk=pk)
    daily_summary_id = expense_instance.daily_summary_id
    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES, instance=expense_instance)
        if form.is_valid():
            form.save()
            if DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
                return redirect(reverse('save_after_submit') + f'?id={daily_summary_id}#7')
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}#7')
        elif DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
            return redirect(reverse('save_after_submit') + f'?id={daily_summary_id}#7')
        else:
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}#7')
    else:
        form = ExpenseForm(instance=expense_instance)
    return render(request, 'edit_expense.html', {'form': form, 'expense_instance': expense_instance})

def edit_bank_deposit(request, pk):
    bank_deposit = get_object_or_404(BankDeposits, pk=pk)
    daily_summary_id = bank_deposit.daily_summary_id
    if request.method == 'POST':
        form = BankDepositsForm(request.POST, request.FILES, instance=bank_deposit)
        if form.is_valid():
            form.save()
            if DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
                return redirect(reverse('save_after_submit') + f'?id={daily_summary_id}#8')
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}#8')
        elif DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
            return redirect(reverse('save_after_submit') + f'?id={daily_summary_id}#8')
        else:
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}#8')
    else:
        form = BankDepositsForm(instance=bank_deposit)
    return render(request, 'edit_bank_deposit.html', {'form': form, 'bank_deposit': bank_deposit})


# def delete_bank_deposit(request, pk):
#     bank_deposit = get_object_or_404(BankDeposits, pk=pk)
#     daily_summary_id = bank_deposit.daily_summary_id
#     bank_deposit.delete()
#     if DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
#         return redirect(reverse('save_after_submit') + f'?id={daily_summary_id}')
#     return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}')

def delete_bank_sale(request, pk):
    try:
        bank_sale = BankSales.objects.get(pk=pk)    
        daily_summary_id = bank_sale.daily_summary_id
        bank_sale.delete()
    except BankSales.DoesNotExist:
        return render(request, '404.html')
    next_page = reverse('create_daily_summary') + f'?id={daily_summary_id}#1'
    if DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
        next_page = reverse('save_after_submit') + f'?id={daily_summary_id}#1'
    return redirect(next_page)


def delete_credit_collection(request, pk):
    try:
        credit = CreditCollection.objects.get(pk=pk)
        daily_summary_id = credit.daily_summary_id
        credit.delete()
    except CreditCollection.DoesNotExist:
        return render(request, '404.html')
    next_page = reverse('create_daily_summary') + f'?id={daily_summary_id}#2'
    if DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
        next_page = reverse('save_after_submit') + f'?id={daily_summary_id}#2'
    return redirect(next_page)

def delete_miscellaneous_income(request, pk):
    try:
        miscellaneous = MiscellaneousIncome.objects.get(pk=pk)
        daily_summary_id = miscellaneous.daily_summary_id
        miscellaneous.delete()
    except MiscellaneousIncome.DoesNotExist:
        return render(request, '404.html')
    next_page = reverse('create_daily_summary') + f'?id={daily_summary_id}#3'
    if DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
        next_page = reverse('save_after_submit') + f'?id={daily_summary_id}#3'
    return redirect(next_page)


def delete_withdrawal(request, pk):
    try:
        withdrawal = Withdrawal.objects.get(pk=pk)
        daily_summary_id = withdrawal.daily_summary_id
        withdrawal.delete()
    except Withdrawal.DoesNotExist:
        return render(request, '404.html')
    next_page = reverse('create_daily_summary') + f'?id={daily_summary_id}#4'
    if DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
        next_page = reverse('save_after_submit') + f'?id={daily_summary_id}#4'
    return redirect(next_page)

def delete_purchase(request, pk):
    try:
        purchase = Purchase.objects.get(pk=pk)
        daily_summary_id = purchase.daily_summary_id
        purchase.delete()
    except Purchase.DoesNotExist:
        return render(request, '404.html')
    next_page = reverse('create_daily_summary') + f'?id={daily_summary_id}#5'
    if DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
        next_page = reverse('save_after_submit') + f'?id={daily_summary_id}#5'
    return redirect(next_page)


def delete_supplier_payment(request, pk):
    try:
        supplier = SupplierPayments.objects.get(pk=pk)
        daily_summary_id = supplier.daily_summary_id
        supplier.delete()
    except SupplierPayments.DoesNotExist:
        return render(request, '404.html')
    next_page = reverse('create_daily_summary') + f'?id={daily_summary_id}#6'
    if DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
        next_page = reverse('save_after_submit') + f'?id={daily_summary_id}#6'
    return redirect(next_page)

def delete_expense(request, pk):
    try:
        expense = Expense.objects.get(pk=pk)
        daily_summary_id = expense.daily_summary_id
        expense.delete()
    except Expense.DoesNotExist:
        return render(request, '404.html')
    next_page = reverse('create_daily_summary') + f'?id={daily_summary_id}#7'
    if DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
        next_page = reverse('save_after_submit') + f'?id={daily_summary_id}#7'
    return redirect(next_page)



def delete_bank_deposit(request, pk):
    try:
        bank_deposit = BankDeposits.objects.get(pk=pk)
        daily_summary_id = bank_deposit.daily_summary_id
        bank_deposit.delete()
    except BankDeposits.DoesNotExist:
        return render(request, '404.html')
    next_page = reverse('create_daily_summary') + f'?id={daily_summary_id}#8'
    if DailySummary.objects.filter(daily_summary_id=daily_summary_id).exists():
        next_page = reverse('save_after_submit') + f'?id={daily_summary_id}#8'
    return redirect(next_page)


# import pisa

def download_pdf_cc(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    api_request = Request(request)
    api_view = DailyCollectionReportAPIView.as_view()
    api_response = api_view(api_request)
    report_data = api_response.data
    html_string = render_to_string('pdf_template_cc.html', {'data': report_data})
    template_path = 'pdf_template_cc.html'
    template = get_template(template_path)
    html = render_to_string('pdf_template_cc.html', {'data': report_data})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{id}.pdf"'

    # pisa_status = pisa.CreatePDF(html, dest=response)
    # if pisa_status.err:
    #     return HttpResponse('We had some errors <pre>' + html + '</pre>')
    
    # with tempfile.NamedTemporaryFile(delete=True) as output:
    #     # HTML(string=html_string).write_pdf(output)
    #     output.seek(0)
    #     pdf = output.read()

    # response = HttpResponse(pdf, content_type='application/pdf')
    # response['Content-Disposition'] = f'attachment; filename="daily_collection_report_{start_date}_to_{end_date}.pdf"'
    return response

class DailyCollectionReportAPIView(APIView):
    def get(self, request):
        start_date = request.GET.get('start_date')
        print('start date1', start_date)
        end_date = request.GET.get('end_date')
        shop_admin = get_object_or_404(ShopAdmin, user=request.user)
        shop = shop_admin.shop
        business_profile = get_object_or_404(BusinessProfile, name=shop.name)
        
        if not start_date or not end_date:
            return Response({'error': 'Please provide start and end dates'}, status=status.HTTP_400_BAD_REQUEST)

        # Parse dates and add timezone info
        start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
        print('end date', end_date)

        # Fetch summaries
        summaries = DailySummary.objects.filter(date__range=[start_date, end_date], business_profile=business_profile.id)
        
        op_bal = DailySummary.objects.filter(date__gte=start_date, business_profile=business_profile.id).first()
        cl_bal = DailySummary.objects.filter(date__range=[start_date, end_date], business_profile=business_profile.id).last()
        # print('cls',cl_bal.values_list('date','opening_balance', 'closing_balance'))
        # print(cl_bal.closing_balance)
        # Initialize totals
        # total_opening_balance = 0
        total_net_collections = 0
        total_net_payments = 0
        total_bank_deposits = 0
        total_closing_balance = 0
        total_msc_income = 0

        opening_summary = DailySummary.objects.filter(date__lte=start_date, business_profile=business_profile.id).order_by('date').first()
     
        opening_balance1 = opening_summary.opening_balance if opening_summary else 0

        for summary in summaries:
            # total_opening_balance = summary.opening_balance or 0
            total_net_collections += summary.credit_collection or 0 
            total_net_payments += (summary.purchase + summary.supplier_payment) or 0 # add the other tables
            total_msc_income += summary.miscellaneous_income or 0
            total_bank_deposits += summary.bank_deposit or 0
            total_closing_balance = summary.closing_balance or 0

        total_closing_balance = (opening_balance1 + total_net_collections + total_msc_income) - (total_net_payments + total_bank_deposits)

        report_data = {
            'start_date': start_date,
            'end_date': end_date,
            'opening_balance': op_bal.opening_balance or 0, #change here
            'net_collections': total_net_collections,
            'net_payments': total_net_payments,
            'msc_income' : total_msc_income,
            'bank_deposits': total_bank_deposits,
            # 'closing_balance': summary.closing_balance,
            'closing_balance': total_closing_balance,
            'details': [
                {
                    'date': summary.date,
                    'net_collections': summary.credit_collection or 0,
                    'net_payments': (summary.purchase + summary.supplier_payment) or 0,
                    'msc_income': summary.miscellaneous_income or 0,
                    'bank_deposits': summary.bank_deposit or 0,
                    'opening_balance': summary.opening_balance,
                    'closing_balance': summary.closing_balance
                } for summary in summaries
            ]
        }

        return JsonResponse(report_data)



class SalesReportAPIView(APIView):

    def get(self, request, *args, **kwargs):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        shop_admin = get_object_or_404(ShopAdmin, user=request.user)
        shop = shop_admin.shop
        business_profile = get_object_or_404(BusinessProfile, name=shop.name)
        
        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch and aggregate data
            sales_data = (
                BankSales.objects.filter(created_on__range=[start_date, end_date], business_profile=business_profile.id)
                .values('created_on__date')
                .annotate(
                    cash=Sum('amount', filter=Q(mode_of_transaction__name='cash')),
                    credit=Sum('amount', filter=Q(mode_of_transaction__name='credit')),
                    card=Sum('amount', filter=Q(mode_of_transaction__name='card')),
                    bank_transfer=Sum('amount', filter=Q(mode_of_transaction__name='bank transfer')),
                    credit_card=Sum('amount', filter=Q(mode_of_transaction__name='credit')),
                    total=Sum('amount')
                )
                .order_by('created_on')
            )
            print('sales', sales_data)
            report_details = [
                {
                    'date': sale['created_on'],
                    'cash': sale['cash'] or 0,
                    'credit': sale['credit'] or 0,
                    'card': sale['card'] or 0,
                    'bank_transfer': sale['bank_transfer'] or 0,
                    'credit_card': sale['credit_card'] or 0,
                    'total': sale['total'] or 0
                } for sale in sales_data
            ]

            summary = {
                'total_cash': sum(sale['cash'] for sale in report_details),
                'total_credit': sum(sale['credit'] for sale in report_details),
                'total_card': sum(sale['card'] for sale in report_details),
                'total_bank_transfer': sum(sale['bank_transfer'] for sale in report_details),
                'total_credit_card': sum(sale['credit_card'] for sale in report_details),
                'total_amount': sum(sale['total'] for sale in report_details)
            }

            return Response({
                'details': report_details,
                'summary': summary
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid date range'}, status=status.HTTP_400_BAD_REQUEST)
        


class PurchaseReportAPIView(APIView):

    def get(self, request, *args, **kwargs):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        shop_admin = get_object_or_404(ShopAdmin, user=request.user)
        shop = shop_admin.shop
        business_profile = get_object_or_404(BusinessProfile, name=shop.name)
        
        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch and aggregate data
            sales_data = (
                Purchase.objects.filter(created_on__range=[start_date, end_date], business_profile=business_profile.id)
                .values('created_on__date')
                .annotate(
                    cash=Sum('invoice_amount', filter=Q(mode_of_transaction__name='cash')),
                    credit=Sum('invoice_amount', filter=Q(mode_of_transaction__name='credit')),
                    card=Sum('invoice_amount', filter=Q(mode_of_transaction__name='card')),
                    bank_transfer=Sum('invoice_amount', filter=Q(mode_of_transaction__name='bank transfer')),
                    credit_card=Sum('invoice_amount', filter=Q(mode_of_transaction__name='credit')),
                    total=Sum('invoice_amount')
                )
                .order_by('created_on')
            )
            print('purchase', sales_data)
            report_details = [
                {
                    'date': sale['created_on'],
                    'cash': sale['cash'] or 0,
                    'credit': sale['credit'] or 0,
                    'card': sale['card'] or 0,
                    'bank_transfer': sale['bank_transfer'] or 0,
                    'credit_card': sale['credit_card'] or 0,
                    'total': sale['total'] or 0
                } for sale in sales_data
            ]

            summary = {
                'total_cash': sum(sale['cash'] for sale in report_details),
                'total_credit': sum(sale['credit'] for sale in report_details),
                'total_card': sum(sale['card'] for sale in report_details),
                'total_bank_transfer': sum(sale['bank_transfer'] for sale in report_details),
                'total_credit_card': sum(sale['credit_card'] for sale in report_details),
                'total_amount': sum(sale['total'] for sale in report_details)
            }

            return Response({
                'details': report_details,
                'summary': summary
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid date range'}, status=status.HTTP_400_BAD_REQUEST)


class MscIncomeReportAPIView(APIView):
    def get(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        shop_admin = get_object_or_404(ShopAdmin, user=request.user)
        shop = shop_admin.shop
        business_profile = get_object_or_404(BusinessProfile, name=shop.name)
        
        # Query the database for Miscellaneous Income within the provided date range
        msc_income = MiscellaneousIncome.objects.filter(created_on__range=[start_date, end_date], business_profile=business_profile.id)
        
        # Prepare the data to be returned
        report_data = {
            'details': [{
                'date': income.created_on,
                'amount': income.amount,
                'income_type': income.receipt_type.name,
                'mode_of_transaction': income.mode_of_transaction.name
            } for income in msc_income],
            'summary': {
                'total_amount': msc_income.aggregate(Sum('amount'))['amount__sum']
            }
        }
        
        return Response(report_data)

class SupplierPaymentReportAPIView(APIView):
    def get(self, request):
        supplier_id = request.GET.get('supplier_id')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        shop_admin = get_object_or_404(ShopAdmin, user=request.user)
        shop = shop_admin.shop
        business_profile = get_object_or_404(BusinessProfile, name=shop.name)
        
        supplier = get_object_or_404(Supplier, id=supplier_id)
        
        # Get supplier payments for the specified supplier
        supplier_payments = SupplierPayments.objects.filter(supplier=supplier, created_on__range=[start_date, end_date], business_profile=business_profile.id)
        
        
        # Calculate total purchases for the supplier within the specified date range

        total_cash_purchases = Purchase.objects.filter(supplier=supplier, invoice_date__range=[start_date, end_date], mode_of_transaction__name='cash').aggregate(Sum('invoice_amount'))['invoice_amount__sum'] or 0
        total_credit_purchases = Purchase.objects.filter(supplier=supplier, invoice_date__range=[start_date, end_date], mode_of_transaction__name='credit').aggregate(Sum('invoice_amount'))['invoice_amount__sum'] or 0
        total_purchases = total_cash_purchases + total_credit_purchases
        
        # Calculate total supplier payments for the specified date range
        total_supplier_payments = supplier_payments.aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Calculate opening balance
        opening_balance = supplier_payments.first().opening_outstanding if supplier_payments.exists() else 0
        
        # Calculate closing balance
        closing_balance = opening_balance + total_purchases - total_supplier_payments
        cash_purchases = Purchase.objects.filter(
            supplier=supplier, 
            invoice_date__range=[start_date, end_date], 
            mode_of_transaction__name='cash', business_profile=business_profile.id
        ).values(
            'invoice_date', 
            'invoice_amount', 
            'mode_of_transaction__name', 
        )

        # Query credit purchases
        credit_purchases = Purchase.objects.filter(
            supplier=supplier, 
            invoice_date__range=[start_date, end_date], 
            mode_of_transaction__name='credit', business_profile=business_profile.id
        ).values(
            'invoice_date', 
            'invoice_amount', 
            'mode_of_transaction__name', 
        )

        # Convert the querysets to lists to make them JSON serializable
        cash_purchases_list = list(cash_purchases)
        credit_purchases_list = list(credit_purchases)

        report_data = {
            'details': {
                'supplier_name': supplier.name,
                'supplier_location': supplier.location,
                'start_date': start_date,
                'end_date': end_date,
                'opening_balance': opening_balance,
                'cash_purchases': cash_purchases_list,
                'credit_purchases': credit_purchases_list,
                'total_cash_purchases': sum(item['invoice_amount'] for item in cash_purchases_list),
                'total_credit_purchases': sum(item['invoice_amount'] for item in credit_purchases_list),
                'total_purchases': total_purchases,
                'total_supplier_payments': total_supplier_payments,
                'closing_balance': closing_balance
            },
            'summary': {
                'total_purchases': total_purchases,
                'total_supplier_payments': total_supplier_payments,
                'closing_balance': closing_balance,
                'opening_balance': opening_balance,
                 'total_cash_purchases': sum(item['invoice_amount'] for item in cash_purchases_list),
                'total_credit_purchases': sum(item['invoice_amount'] for item in credit_purchases_list),
            }
        }
        
        return Response(report_data)
    
class BankStatementAPIView(APIView):
    def get(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        bank_id = request.GET.get('bank')
        shop_admin = get_object_or_404(ShopAdmin, user=request.user)
        shop = shop_admin.shop
        business_profile = get_object_or_404(BusinessProfile, name=shop.name)

        if not (start_date and end_date and bank_id):
            return Response({'error': 'Invalid parameters'}, status=400)

        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()  # Convert to date object
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()  # Convert to date object
        bank = get_object_or_404(Bank, id=bank_id)

        def get_transactions(model, date_field, amount_field, description_field, bank_field=None):
            filters = {
                date_field + '__range': [start_date, end_date],
                'business_profile': business_profile.id,
            }
            if bank_field:
                filters[bank_field] = bank
            else:
                filters['bank'] = bank
            
            transactions = model.objects.filter(
                Q(**filters)
            ).annotate(
                description=F(description_field),
                amount=Sum(amount_field)
            ).values(date_field, 'description', 'amount')

            # Ensure the date is a `date` object
            for transaction in transactions:
                if isinstance(transaction[date_field], datetime):
                    transaction[date_field] = transaction[date_field].date()

            return transactions

        # Aggregating data from various models
        deposits = get_transactions(BankDeposits, 'deposit_date', 'amount', 'mode_of_transaction__name', 'bank_deposit_bank')
        withdrawals = get_transactions(Withdrawal, 'withdrawal_date', 'amount', 'mode_of_transaction__name', 'bank')
        purchases = get_transactions(Purchase, 'invoice_date', 'invoice_amount', 'mode_of_transaction__name', 'bank')
        # expenses = get_transactions(Expense, 'created_on', 'amount', 'mode_of_transaction__name', 'bank')

        # Convert querysets to lists and process them
        transactions_list = []
        for transactions, date_field, amount_key, type_key in [
            (deposits, 'deposit_date', 'deposit', 'Deposit'),
            (withdrawals, 'withdrawal_date', 'withdrawal', 'Withdrawal'),
            (purchases, 'invoice_date', 'purchase', 'Purchase'),
            # (expenses, 'created_on', 'expense', 'Expense')
        ]:
            for transaction in transactions:
                transactions_list.append({
                    'date': transaction[date_field],
                    'description': transaction['description'],
                    amount_key: transaction['amount'],
                    'transaction_type': type_key
                })

        # Sort all transactions by date
        all_transactions = sorted(
            transactions_list,
            key=lambda x: x['date']
        )

        statement_details = []
        opening_balance = bank.opening_balance
        balance = opening_balance
        total_deposits = 0
        total_withdrawals = 0

        # Add opening balance entry
        statement_details.append({
            'date': start_date.strftime('%d %b %Y'),
            'description': 'Opening Balance',
            'withdrawal': 0,
            'deposit': 0,
            'balance': opening_balance
        })

        for transaction in all_transactions:
            date = transaction['date']
            formatted_date = date.strftime('%d %b %Y')
            deposit = transaction.get('deposit', 0)
            withdrawal = transaction.get('withdrawal', 0)
            purchase = transaction.get('purchase', 0)
            # expense = transaction.get('expense', 0)

            # Update balance
            balance += deposit - withdrawal - purchase 

            statement_details.append({
                'date': formatted_date,
                'description': transaction['description'],
                'withdrawal': withdrawal + purchase,
                'deposit': deposit,
                'balance': balance
            })

            total_deposits += deposit
            total_withdrawals += withdrawal + purchase 

        # Prepare the response
        return Response({
            'details': statement_details,
            'summary': {
                'total_deposits': total_deposits,
                'total_withdrawals': total_withdrawals,
                'final_balance': balance
            }
        })