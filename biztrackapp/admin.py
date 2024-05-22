from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    model = User

    list_display = ('username', 'email', 'is_active',
                    'is_staff', 'is_superuser', 'last_login','is_admin',)
    
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'date_joined')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2','first_name','last_name', 'is_staff', 'is_active','country_code','phone_number','is_admin')}
         ),
    )
    search_fields = ('email','username')
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)

admin.site.register(Shop)
admin.site.register(ShopAdmin)

class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'license_number', 'license_expiration', 'shop_phone_number', 'vat_percentage', 'vat_number', 'created_on')
    search_fields = ('name', 'license_number', 'vat_number')
    list_filter = ('license_expiration', 'vat_submission_date_1', 'vat_submission_date_2', 'vat_submission_date_3')
    readonly_fields = ('created_on',)

admin.site.register(BusinessProfile, BusinessProfileAdmin)


@admin.register(ExpenseType)
class ExpenseTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_on']

@admin.register(ReceiptType)
class ReceiptTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_on']

@admin.register(TransactionMode)
class TransactionModeAdmin(admin.ModelAdmin):
    list_display = ['name', 'business_profile','created_on']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name','outstanding', 'location', 'business_profile', 'status', 'created_on')
    list_filter = ('status',)
    search_fields = ('name', 'location')
    readonly_fields = ('created_on',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display =('name','outstanding', 'location', 'business_profile', 'status', 'created_on')
    list_filter = ('status',)
    search_fields = ('name', 'location')
    readonly_fields = ('created_on',)


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ['name','account_number','opening_balance', 'business_profile','created_on']



admin.site.register(Employee)