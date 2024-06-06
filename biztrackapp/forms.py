from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import *

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email','country_code','phone_number','is_admin')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        # fields = ('email',)
        fields = ('email','country_code','phone_number','is_admin')


class BusinessProfileForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     # Get the user from the form kwargs
    #     user = kwargs.pop('user', None)
    #     super(BusinessProfileForm, self).__init__(*args, **kwargs)
    #     if user and not user.is_superuser:
    #         # Filter shop choices based on the currently logged-in user's associated shop
    #         self.fields['shop'].queryset = Shop.objects.filter(admin_user=user)

    class Meta:
        model = BusinessProfile
        fields = '__all__'

class BusinessTimingForm(forms.ModelForm):
    class Meta:
        model = BusinessTiming
        fields = '__all__'
        widgets = {
            'business_start_time': forms.TimeInput(attrs={'type': 'time'}),
            'business_end_time': forms.TimeInput(attrs={'type': 'time'}),
        }


class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partners
        fields = ['shop', 'user', 'business_profile', 'email_1', 'email_2', 'email_3', 'mobile_1', 'mobile_2', 'mobile_3']

class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = Withdrawal
        fields = ['bank', 'withdrawal_date', 'amount', 'mode_of_transaction', 'daily_summary_id', 'business_profile']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mode_of_transaction'].queryset = TransactionMode.objects.exclude(name__in=['credit','bank transfer','card'])
        
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'outstanding', 'location', 'business_profile', 'status']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'outstanding', 'location', 'business_profile', 'status']

class ExpenseTypeForm(forms.ModelForm):
    class Meta:
        model = ExpenseType
        fields = '__all__'

class ReceiptTypeForm(forms.ModelForm):
    class Meta:
        model = ReceiptType
        fields = '__all__'

class BankForm(forms.ModelForm):
    name = forms.ChoiceField(choices=BANK_CHOICES, label="Bank Name")

    class Meta:
        model = Bank
        fields = '__all__'

class AllBankForm(forms.ModelForm):
    name = forms.ChoiceField(choices=BANK_CHOICES, label="Bank Name")

    class Meta:
        model = AllBank
        fields = '__all__'

class ModeofTransactionForm(forms.ModelForm):
    class Meta:
        model = TransactionMode
        fields = '__all__'


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields ='__all__'

class DailySummaryForm(forms.ModelForm):
    class Meta:
        model = DailySummary
        fields = '__all__'
    closing_balance = forms.DecimalField(required=False)



class BankSaleForm(forms.ModelForm):
    class Meta:
        model = BankSales
        fields = '__all__'

class CreditCollectionForm(forms.ModelForm):
    class Meta:
        model = CreditCollection
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['payment_mode'].queryset = TransactionMode.objects.exclude(name__in=['credit'])

class MiscellaneousIncomeForm(forms.ModelForm):
    class Meta:
        model = MiscellaneousIncome
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mode_of_transaction'].queryset = TransactionMode.objects.exclude(name__in=['credit'])

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = '__all__'

class SupplierPaymentForm(forms.ModelForm):
    class Meta:
        model = SupplierPayments
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mode_of_transaction'].queryset = TransactionMode.objects.exclude(name__in=['credit'])


class BankDepositsForm(forms.ModelForm):
    class Meta:
        model = BankDeposits
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mode_of_transaction'].queryset = TransactionMode.objects.exclude(name__in=['credit'])


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mode_of_transaction'].queryset = TransactionMode.objects.exclude(name__in=['credit'])