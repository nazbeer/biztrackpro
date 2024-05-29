from django.db import models
from django.contrib.auth.models import AbstractUser


class Shop(models.Model):
    name = models.CharField(max_length=255, verbose_name='Shop Name')
    license_number = models.CharField(max_length=50, unique=True)
    num_users = models.PositiveIntegerField(verbose_name='Number of Users')
    vat_remainder = models.BooleanField(default=True, verbose_name='VAT Reminder')
    employee_transaction_window = models.BooleanField(default=True)
    license_expiration_reminder = models.BooleanField(default=True, verbose_name='License Expiration Reminder')
    employee_visa_expiration_reminder = models.BooleanField(default=True, verbose_name='Employee Visa Expiration Reminder')
    employee_passport_expiration_reminder = models.BooleanField(default=True, verbose_name='Employee Passport Expiration Reminder')
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name}"

class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    country_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)
    is_admin = models.BooleanField(default=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return f"{self.username}"

class ShopAdmin(models.Model):
    shop = models.ForeignKey(Shop,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"Shop {self.shop.name} - user {self.user.username}"


class BusinessProfile(models.Model):
    name = models.CharField(max_length=64, blank=False, default=None, null=True)
    # shop = models.ForeignKey(Shop,on_delete=models.CASCADE)
    license_number = models.CharField(max_length=255)
    license_expiration = models.DateField(null=True)
    license_upload = models.FileField(upload_to='licenses')
    shop_phone_number = models.CharField(max_length=25)
    vat_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    vat_number = models.CharField(max_length=255)
    vat_submission_date_1 = models.DateField(null=True)
    vat_submission_date_2 = models.DateField(null=True)
    vat_submission_date_3 = models.DateField(null=True)
    vat_certificate_upload = models.FileField(upload_to='vat_certificates')
    address = models.TextField()
    license_expiration_reminder_days = models.PositiveIntegerField(verbose_name='License Expiration Reminder (days)')
    vat_submission_date_reminder_days = models.PositiveIntegerField(null=True, verbose_name='VAT Submission Date Reminder (days)')
    employee_visa_expiration_reminder_days = models.PositiveIntegerField(null=True, verbose_name='Employee Visa Expiration Reminder (days)')
    employee_passport_expiration_reminder_days = models.PositiveIntegerField(null=True, verbose_name='Employee Passport Expiration Reminder (days)')
    # business_start_time = models.TimeField(null=True, blank=True)
    # business_end_time = models.TimeField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return f" {self.name}"

class Employee(models.Model):
    employee_id = models.CharField(max_length=10, unique=True)
    # business_profile = models.ForeignKey(BusinessProfile,on_delete=models.CASCADE)
    business_profile = models.CharField(max_length=255, null=True)
    business_profile_id = models.IntegerField(null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    nationality = models.CharField(max_length=255)
    mobile_no = models.CharField(max_length=20, blank=True, null=True)
    passport_no = models.CharField(max_length=20, unique=True)
    passport_expiration_date = models.DateField(null=True)
    emirates_id = models.CharField(max_length=20, unique=True)
    id_expiration_date = models.DateField()
    basic_pay = models.DecimalField(max_digits=10, decimal_places=2)
    house_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transportation_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    joining_date = models.DateField()
    job_role = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.business_profile} - {self.employee_id} - {self.first_name} {self.last_name}"
    
class BusinessTiming(models.Model):
    business_profile = models.ForeignKey(BusinessProfile,on_delete=models.CASCADE, null=True)
    business_start_time = models.TimeField(null=True, blank=True)
    business_end_time = models.TimeField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)
    def __str__(self):
        return f"{self.business_profile} - {self.business_start_time} - {self.business_end_time}"
    
class ExpenseType(models.Model):
    name = models.CharField(max_length=255)
    business_profile = models.CharField(max_length=255, null=True)
    status = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name}"

class ReceiptType(models.Model):
    name = models.CharField(max_length=255)
    business_profile = models.CharField(max_length=255, null=True)
    status = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name}"

class Bank(models.Model):
    name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50)
    opening_balance = models.DecimalField(max_digits=10, decimal_places=2)
    business_profile = models.CharField(max_length=255, null=True)
    status = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name}"

class TransactionMode(models.Model):
    CHOICES = [
        ('card', 'Card'),
        ('cash', 'Cash'),
        ('bank', 'Bank Transfer'),
        ('cheque', 'Cheque'),
        ('credit', 'Credit'),

    ]
    name = models.CharField(max_length=255,choices=CHOICES)
    business_profile = models.CharField(max_length=255, null=True)
    status = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name}"

class Customer(models.Model):
    name = models.CharField(max_length=255)
    business_profile = models.CharField(max_length=255, null=True)
    outstanding = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    status = models.BooleanField(default=True)  # BooleanField to represent True or False
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    business_profile = models.CharField(max_length=255, null=True)
    outstanding = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    status = models.BooleanField(default=True)  # BooleanField to represent True or False
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.business_profile} - {self.name}"


class DailySummary(models.Model):
    CHOICES = [
        ('completed', 'Completed'),
        ('ongoing', 'On going'),
    ]
    date = models.DateField()
    opening_balance = models.DecimalField(max_digits=10, decimal_places=2)
    daily_summary_id = models.CharField(max_length=100, null=True, blank=True)
    cash_sale = models.DecimalField(max_digits=10, decimal_places=2)
    credit_sale = models.DecimalField(max_digits=10, decimal_places=2)
    card_sale = models.DecimalField(max_digits=10, decimal_places=2)
    sales = models.DecimalField(max_digits=10, decimal_places=2)
    credit_collection = models.DecimalField(max_digits=10, decimal_places=2)
    miscellaneous_income = models.DecimalField(max_digits=10, decimal_places=2)
    purchase = models.DecimalField(max_digits=10, decimal_places=2)
    supplier_payment = models.DecimalField(max_digits=10, decimal_places=2)
    expense = models.DecimalField(max_digits=10, decimal_places=2)
    bank_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    closing_balance = models.DecimalField(max_digits=10, decimal_places=2)
    business_profile = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=20, choices=CHOICES)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.date} {self.status}"
    
class BankSales(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    daily_summary_id = models.CharField(max_length=100, null=True, blank=True)
    mode_of_transaction = models.ForeignKey(TransactionMode, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    cheque_date = models.DateField()
    cheque_no = models.CharField(max_length=255)
    business_profile = models.CharField(max_length=255, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.name} - {self.amount}"

class CreditCollection(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    daily_summary_id = models.CharField(max_length=100, null=True, blank=True)
    payment_mode = models.ForeignKey(TransactionMode, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    cheque_date = models.DateField()
    cheque_no = models.CharField(max_length=255)
    business_profile = models.CharField(max_length=255, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.name} - {self.amount}"

class MiscellaneousIncome(models.Model):
    receipt_type = models.ForeignKey(ReceiptType, on_delete=models.CASCADE)
    daily_summary_id = models.CharField(max_length=100, null=True, blank=True)
    mode_of_transaction = models.ForeignKey(TransactionMode, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    cheque_date = models.DateField()
    cheque_no = models.CharField(max_length=255)
    business_profile = models.CharField(max_length=255, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.amount}"

class Purchase(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    daily_summary_id = models.CharField(max_length=100, null=True, blank=True)
    opening_outstanding = models.DecimalField(max_digits=10, decimal_places=2)
    mode_of_transaction = models.ForeignKey(TransactionMode, on_delete=models.CASCADE)
    invoice_date = models.DateField()
    invoice_no = models.CharField(max_length=255)
    invoice_amount = models.DecimalField(max_digits=10, decimal_places=2)
    cheque_date = models.DateField()
    cheque_no = models.CharField(max_length=255)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    business_profile = models.CharField(max_length=255, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Invoice {self.invoice_no} - {self.supplier.name}"

class SupplierPayments(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    daily_summary_id = models.CharField(max_length=100, null=True, blank=True)
    opening_outstanding = models.DecimalField(max_digits=10, decimal_places=2)
    mode_of_transaction = models.ForeignKey(TransactionMode, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    cheque_date = models.DateField()
    cheque_no = models.CharField(max_length=255)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    business_profile = models.CharField(max_length=255, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Amount {self.amount} - {self.supplier.name}"
    

class BankDeposits(models.Model):
    bank_deposit_bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='deposits_as_bank_deposit')
    daily_summary_id = models.CharField(max_length=100, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='deposits_as_bank')
    deposit_date = models.DateField()
    mode_of_transaction = models.ForeignKey(TransactionMode, on_delete=models.CASCADE)
    cheque_date = models.DateField()
    cheque_no = models.CharField(max_length=255)
    business_profile = models.CharField(max_length=255, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.amount}"


class Expense(models.Model):
    expense_type = models.ForeignKey(ExpenseType, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    daily_summary_id = models.CharField(max_length=100, null=True, blank=True)
    cheque_no = models.CharField(max_length=255,null=True,blank=True)
    invoice_no = models.CharField(max_length=255)
    mode_of_transaction = models.ForeignKey(TransactionMode, on_delete=models.CASCADE)
    cheque_date = models.DateField()
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    business_profile = models.CharField(max_length=255, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.amount}"

