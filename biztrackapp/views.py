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


def index(request):
    print('re',request.user)
    user = request.user
    business = ShopAdmin.objects.get(user = user)
    return HttpResponse(f"{user}  {business}")




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
                'name': 'Role Management',
                # 'links': [
                #     {'label': 'Create Role', 'url_name': 'create_role'},
                #     {'label': 'Role List', 'url_name': 'role_list'},
                   
                # ]
            },
            {
                'name': 'Employee Management',
                'links': [
                        # {'label': 'Create Employee', 'url_name': 'create_employee'},
                        # {'label': 'Employee List', 'url_name': 'employee_list'},
                  
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
            form.save()
            return redirect('bank_list')  
    else:
        form = BankForm()

    context = {
        'form': form,
        'business_profile': business_profile.id,
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
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_type_list')
    else:
        form = EmployeeForm()
    return render(request, 'create_employee.html', {'form': form,'business_profile':business_profile.id})
