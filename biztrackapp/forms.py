from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import *

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email','country_code','phone_number','is_admin','is_employee')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        # fields = ('email',)
        fields = ('email','country_code','phone_number','is_admin','is_employee')

class ShopAdminForm(forms.ModelForm):
    class Meta:
        model = ShopAdmin
        fields = ['shop', 'user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(is_admin=True)

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
        fields = ['bank', 'withdrawal_date', 'amount', 'mode_of_transaction', 'daily_summary_id', 'business_profile','cheque_date','cheque_no']
        amount = forms.DecimalField(
            widget=forms.TextInput(attrs={'class': 'form-control', 'tabindex': '1503', 'required': True})
        )

    def __init__(self, *args, **kwargs):
        business_profile = kwargs.pop('business_profile', None)
        super().__init__(*args, **kwargs)
        self.fields['bank'].queryset = Bank.objects.filter(business_profile=business_profile)
        self.fields['mode_of_transaction'].queryset = TransactionMode.objects.filter(business_profile=business_profile).exclude(name__in=['credit','bank transfer','card'])
        
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
    # name = forms.ChoiceField(choices=BANK_CHOICES, label="Bank Name")

    class Meta:
        model = Bank
        fields = '__all__'
        
    def clean(self):
        cleaned_data = super().clean()
        bank = cleaned_data.get('bank')
        business_profile = cleaned_data.get('business_profile')

        if Bank.objects.filter(bank=bank, business_profile=business_profile).exists():
            raise forms.ValidationError("This AllBank instance is already associated with this business profile.")

        return cleaned_data


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
    country_code = forms.CharField()
    phone_number = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField()
    class Meta:
        model = Employee
        fields =[
            'employee_id',
            'first_name',
            'last_name',
            'email',
            'business_profile',
            'business_profile_id',
            'nationality',
            'mobile_no',
            'passport_no',
            'passport_expiration_date',
            'emirates_id',
            'id_expiration_date',
            'basic_pay',
            'house_allowance',
            'transportation_allowance',
            'joining_date',
            'job_role',
            'email',
            'country_code' ,
            'phone_number' ,
            'password',
            'status'
        ]

class DailySummaryForm(forms.ModelForm):
    class Meta:
        model = DailySummary
        fields = '__all__'
    closing_balance = forms.DecimalField(required=False)



class BankSaleForm(forms.ModelForm):
    class Meta:
        model = BankSales
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        business_profile = kwargs.pop('business_profile', None)
        super().__init__(*args, **kwargs)
        self.fields['mode_of_transaction'].queryset = TransactionMode.objects.filter(business_profile=business_profile,status=True)
        self.fields['customer'].queryset = Customer.objects.filter(business_profile=business_profile, status=True)


class CreditCollectionForm(forms.ModelForm):
    class Meta:
        model = CreditCollection
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        business_profile = kwargs.pop('business_profile', None)
        super().__init__(*args, **kwargs)
        self.fields['payment_mode'].queryset = TransactionMode.objects.filter(business_profile=business_profile,status=True).exclude(name__in=['credit'])
        self.fields['customer'].queryset = Customer.objects.filter(business_profile=business_profile, status=True)


class MiscellaneousIncomeForm(forms.ModelForm):
    class Meta:
        model = MiscellaneousIncome
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        business_profile = kwargs.pop('business_profile', None)
        super().__init__(*args, **kwargs)
        self.fields['mode_of_transaction'].queryset = TransactionMode.objects.filter(business_profile=business_profile,status=True).exclude(name__in=['credit'])
        self.fields['receipt_type'].queryset = ReceiptType.objects.filter(business_profile=business_profile,status=True)

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        business_profile = kwargs.pop('business_profile', None)
        super().__init__(*args, **kwargs)
        self.fields['mode_of_transaction'].queryset = TransactionMode.objects.filter(business_profile=business_profile,status = True)
        self.fields['supplier'].queryset = Supplier.objects.filter(business_profile=business_profile, status = True)


class SupplierPaymentForm(forms.ModelForm):
    class Meta:
        model = SupplierPayments
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        business_profile = kwargs.pop('business_profile', None)
        super().__init__(*args, **kwargs)
        self.fields['mode_of_transaction'].queryset = TransactionMode.objects.filter(business_profile=business_profile,status = True).exclude(name__in=['credit'])
        self.fields['bank'].queryset = Bank.objects.filter(business_profile=business_profile,status = True)
        self.fields['supplier'].queryset = Supplier.objects.filter(business_profile=business_profile, status = True)


class BankDepositsForm(forms.ModelForm):
    class Meta:
        model = BankDeposits
        fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['mode_of_transaction'].queryset = TransactionMode.objects.exclude(name__in=['credit'])

    def __init__(self, *args, **kwargs):
        business_profile = kwargs.pop('business_profile', None)
        super().__init__(*args, **kwargs)
        self.fields['mode_of_transaction'].queryset = TransactionMode.objects.filter(business_profile=business_profile,status = True).exclude(name__in=['credit'])
        self.fields['bank_deposit_bank'].queryset = Bank.objects.filter(business_profile=business_profile,status = True)



class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = '__all__'
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['mode_of_transaction'].queryset = TransactionMode.objects.exclude(name__in=['credit'])
    def __init__(self, *args, **kwargs):
        business_profile = kwargs.pop('business_profile', None)
        super().__init__(*args, **kwargs)
        self.fields['mode_of_transaction'].queryset = TransactionMode.objects.filter(business_profile=business_profile,status = True).exclude(name__in=['credit'])
        self.fields['expense_type'].queryset = ExpenseType.objects.filter(business_profile=business_profile,status = True)
