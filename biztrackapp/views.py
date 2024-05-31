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
from django.db.models import Count, Sum, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from django.http import JsonResponse

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
                'name': 'Shop & Profile Management',
                'links': [
                    {'label': 'Profile', 'url_name': 'home'},
                    {'label': 'Shop', 'url_name': 'home'},
                   
                ]
            },
            {
                'name': 'Shop Management',
                'links': [
                    {'label': 'Create Business', 'url_name': 'create_business_profile'},
                    {'label': 'Business Profiles', 'url_name': 'business_profile_list'},
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
        'bank_choices': BANK_CHOICES
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

from datetime import date
from django.db.models import Max
def create_daily_summary(request):
    id = request.GET.get('id')
    today = date.today()
    shop_admin = get_object_or_404(ShopAdmin, user=request.user)
    shop = shop_admin.shop
    # Retrieve the business profile associated with the shop
    business_profile = get_object_or_404(BusinessProfile, name=shop.name)
    business_timing = BusinessTiming.objects.filter(business_profile=business_profile.id).first()
    if request.method == 'POST':
        form = DailySummaryForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.daily_summary_id = id  # Assign the value here
            instance.save()
            return redirect('daily_summary_list')
    else:
        form = DailySummaryForm()
        bank_sale_form = BankSaleForm()
        credit_collection_form = CreditCollectionForm()
        msc_income_form = MiscellaneousIncomeForm()
        purchase_form = PurchaseForm()
        supplier_payments_form = SupplierPaymentForm()
        bank_deposit_form = BankDepositsForm()
        expense_form = ExpenseForm()

    try:
        # Get the latest DailySummary by sorting by date in descending order and taking the first one
        daily_summary = DailySummary.objects.latest('date')
        bankdata = daily_summary.closing_balance
    except DailySummary.DoesNotExist:
        # If no DailySummary exists at all, get the opening balance from BusinessProfile
        bankdata = business_profile.opening_balance

    daily_summary = DailySummary.objects.filter(business_profile=business_profile.id)

    # bankdata = business_profile.opening_balance
    

    # Query for bank sales created on the current date
    bank_sales = BankSales.objects.filter(business_profile=business_profile.id, daily_summary_id = id)
    credit_collections = CreditCollection.objects.filter(business_profile=business_profile.id, daily_summary_id = id)
    msc_income = MiscellaneousIncome.objects.filter(business_profile=business_profile.id, daily_summary_id = id)
    purchases = Purchase.objects.filter(business_profile=business_profile.id, daily_summary_id = id)
    supplier_payments = SupplierPayments.objects.filter(business_profile=business_profile.id, daily_summary_id = id)
    expense = Expense.objects.filter(business_profile=business_profile.id, daily_summary_id = id)
    bank_deposit = BankDeposits.objects.filter(business_profile=business_profile.id, daily_summary_id = id)

    expense_type = ExpenseType.objects.filter(business_profile=business_profile.id)
    receipt_type = ReceiptType.objects.filter(business_profile=business_profile.id)

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
        bank_transaction_mode = TransactionMode.objects.get(name="bank")
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

            #cash on hand
            'cash_on_hand':bankdata,

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

    
            'id': id


        }
    )





def create_bank_sale(request):
    if request.method == 'POST':
        form = BankSaleForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            daily_summary_id = request.POST.get('daily_summary_id')  # Get the daily summary ID from the form
            form.daily_summary_id = daily_summary_id  # Assign the daily summary ID to the bank sale instance
            form.save()
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}')
           
    return redirect('create_daily_summary')

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
        if form.is_valid():
            form = form.save(commit=False)
            daily_summary_id = request.POST.get('daily_summary_id')  # Get the daily summary ID from the form
            form.daily_summary_id = daily_summary_id  # Assign the daily summary ID to the bank sale instance
            form.save()
            # Redirect to the 'create_daily_summary' URL with the dailySummaryId in the query parameters
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}')
    return redirect('create_daily_summary')

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
        if form.is_valid():
            form = form.save(commit=False)
            daily_summary_id = request.POST.get('daily_summary_id')  # Get the daily summary ID from the form
            form.daily_summary_id = daily_summary_id  # Assign the daily summary ID to the bank sale instance
            form.save()
            # Redirect to the 'create_daily_summary' URL with the dailySummaryId in the query parameters
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}')
    return redirect('create_daily_summary')

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
        if form.is_valid():
            form = form.save(commit=False)
            daily_summary_id = request.POST.get('daily_summary_id')  # Get the daily summary ID from the form
            form.daily_summary_id = daily_summary_id  # Assign the daily summary ID to the bank sale instance
            form.save()
            # Redirect to the 'create_daily_summary' URL with the dailySummaryId in the query parameters
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}')
    return redirect('create_daily_summary')

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
        if form.is_valid():
            form = form.save(commit=False)
            daily_summary_id = request.POST.get('daily_summary_id')  # Get the daily summary ID from the form
            form.daily_summary_id = daily_summary_id  # Assign the daily summary ID to the bank sale instance
            form.save()
            # Redirect to the 'create_daily_summary' URL with the dailySummaryId in the query parameters
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}')
    return redirect('create_daily_summary')

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
        if form.is_valid():
            form = form.save(commit=False)
            daily_summary_id = request.POST.get('daily_summary_id')  # Get the daily summary ID from the form
            form.daily_summary_id = daily_summary_id  # Assign the daily summary ID to the bank sale instance
            form.save()
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}')
    return redirect('create_daily_summary')

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
        if form.is_valid():
            form = form.save(commit=False)
            daily_summary_id = request.POST.get('daily_summary_id')  # Get the daily summary ID from the form
            form.daily_summary_id = daily_summary_id  # Assign the daily summary ID to the bank sale instance
            form.save()
            return redirect(reverse('create_daily_summary') + f'?id={daily_summary_id}')
    return redirect('create_daily_summary')

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