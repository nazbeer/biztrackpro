from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm,ShopAdminForm
from .models import *


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    model = User

    list_display = ('username', 'email', 'is_active',
                    'is_staff', 'is_superuser', 'last_login','is_admin','is_employee')
    
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

@admin.register(Shop)
class NewShopAdmin(admin.ModelAdmin):
    list_display = ['name','license_number', 'num_users','vat_remainder', 'employee_transaction_window', 'license_expiration_reminder', 'employee_visa_expiration_reminder', 'employee_passport_expiration_reminder', 'created_on']

# @admin.register(ShopAdmin)
# class ShopAdminAdmin(admin.ModelAdmin):
#     list_display = ['shop', 'user']
class ShopAdminAdmin(admin.ModelAdmin):
    form = ShopAdminForm
    list_display = ['shop', 'user']
admin.site.register(ShopAdmin, ShopAdminAdmin)

class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'license_number', 'license_expiration', 'shop_phone_number', 'vat_percentage', 'vat_number', 'created_on')
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
    list_display = ['id','bank','account_number','opening_balance', 'business_profile','created_on', 'update_on']



admin.site.register(Employee)
@admin.register(DailySummary)
class DailySummaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'daily_summary_id', 'date', 'status', 'opening_balance', 'cash_sale', 'credit_sale', 'card_sale', 'sales', 'credit_collection', 'miscellaneous_income', 'purchase', 'supplier_payment', 'expense', 'bank_deposit', 'closing_balance', 'business_profile', 'created_on', 'updated_on')
    list_filter = ('status', 'date', 'business_profile')
    search_fields = ('business_profile', 'daily_summary_id')
    ordering = ('-date',)

@admin.register(BankSales)
class BankSaleAdmin(admin.ModelAdmin):
    list_display = ['id','daily_summary_id', 'customer','mode_of_transaction','amount', 'bank','cheque_date', 'cheque_no', 'created_on','updated_on']

@admin.register(BankDeposits)
class BankDepositAdmin(admin.ModelAdmin):
    list_display = ['id', 'daily_summary_id', 'bank_deposit_bank','mode_of_transaction','amount', 'bank','deposit_date','cheque_date', 'cheque_no','business_profile', 'created_on', 'updated_on']

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['id', 'daily_summary_id', 'expense_type','mode_of_transaction','amount', 'bank','cheque_date', 'cheque_no','invoice_no','business_profile',  'created_on', 'updated_on']


@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ['id', 'daily_summary_id','mode_of_transaction','amount', 'bank','withdrawal_date','cheque_date', 'cheque_no','business_profile', 'created_on', 'updated_on']

@admin.register(AllBank)
class AllBankAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','created_on', 'update_on']

@admin.register(CreditCollection)
class CreditCollectionAdmin(admin.ModelAdmin):
    list_display = ['id','daily_summary_id', 'customer','payment_mode','amount', 'bank','cheque_date', 'cheque_no','business_profile', 'created_on', 'updated_on']

@admin.register(MiscellaneousIncome)
class MiscellaneousIncomeAdmin(admin.ModelAdmin):
    list_display = ['id', 'daily_summary_id','mode_of_transaction','receipt_type','amount', 'bank','cheque_date', 'cheque_no','business_profile', 'created_on', 'updated_on']
@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):  
    list_display = ['id','daily_summary_id', 'supplier','mode_of_transaction','invoice_date','invoice_no','invoice_amount', 'bank','cheque_date', 'cheque_no','business_profile', 'created_on', 'updated_on']

@admin.register(SupplierPayments)
class SupplierPaymentsAdmin(admin.ModelAdmin):
    list_display = ['id','daily_summary_id', 'supplier','mode_of_transaction','amount', 'bank','business_profile','opening_outstanding','cheque_date', 'cheque_no', 'created_on', 'updated_on']

admin.site.register(BusinessTiming)
admin.site.register(Partners)



