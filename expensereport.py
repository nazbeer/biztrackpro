import os
import django
import csv
from datetime import datetime, date
import random
import string

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biztrackpro.settings')
django.setup()

from biztrackapp.models import DailySummary, Expense, ExpenseType, TransactionMode, Bank

def generate_random_summary_id():
    return "DS_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

# Create a mapping of date to daily_summary_id
date_to_summary_id = {ds.date: ds.daily_summary_id for ds in DailySummary.objects.filter(business_profile=2)}

# Clear existing Expense entries
Expense.objects.filter(business_profile=2).delete()

# Reset the auto-increment id counter for SQLite
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='biztrackapp_expense';")

# Load the data from the Expense CSV file
expense_file_path = 'expense1.csv'  # Path to the uploaded CSV file

# Print headers to debug
with open(expense_file_path, mode='r') as file:
    csv_reader = csv.DictReader(file)
    headers = csv_reader.fieldnames
    print(headers)

# Load Expense data
expenses = []
with open(expense_file_path, mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        expense_date = datetime.strptime(row["date"], "%Y-%m-%d").date()
        daily_summary_id = date_to_summary_id.get(expense_date)

        if daily_summary_id:
            expense = Expense(
                expense_type=ExpenseType.objects.get(id=row["expense_type"]),
                amount=row["amount"],
                daily_summary_id=daily_summary_id,
                cheque_no=None,  # Ensure cheque_no is set to None for all entries
                invoice_no=row["invoice_no"],
                mode_of_transaction=TransactionMode.objects.get(name='cash', business_profile=2),  # Filter by business_profile
                cheque_date=expense_date,
                bank=Bank.objects.get(id=1),
                business_profile=2,
                created_on=expense_date,  # Override auto_now_add
                updated_on=date.today()
            )
            expenses.append(expense)

# Bulk create the Expense entries
Expense.objects.bulk_create(expenses)

# Manually set the created_on field using a direct update
for expense in expenses:
    Expense.objects.filter(pk=expense.pk).update(created_on=expense.created_on)
