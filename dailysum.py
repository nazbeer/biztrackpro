import os
import django
import csv
from datetime import datetime, date
import random
import string

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biztrackpro.settings')
django.setup()

from biztrackapp.models import DailySummary

def generate_random_summary_id():
    return "DS_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

# Clear existing entries
DailySummary.objects.filter(business_profile=2).delete()

# Reset the auto-increment id counter for SQLite
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='biztrackapp_dailysummary';")

# Load the data from the CSV file
file_path = 'ds.csv'  # Path to the uploaded CSV file

with open(file_path, mode='r') as file:
    csv_reader = csv.DictReader(file)
    headers = csv_reader.fieldnames
    print(headers)

daily_summaries = []
with open(file_path, mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        daily_summary = DailySummary(
            date=datetime.strptime(row["date"], "%Y-%m-%d").date(),
            daily_summary_id=generate_random_summary_id(),
            opening_balance=row[" opening_balance "].replace(",", ""),
            cash_sale=row[" cash_sale "].replace(",", ""),
            card_sale=row[" card_sale "].replace(",", ""),
            credit_sale=row[" credit_sale "].replace(",", ""),
            sales=row[" sales "].replace(",", ""),
            credit_collection=row[" credit_collection "].replace(",", ""),
            miscellaneous_income=row[" miscellaneous_income "].replace(",", ""),
            purchase=row[" purchase "].replace(",", ""),
            supplier_payment=row[" supplier_payment "].replace(",", ""),
            expense=row[" expense "].replace(",", ""),
            withdrawal=row[" withdrawal "].replace(",", ""),
            bank_deposit=row[" bank_deposit "].replace(",", ""),
            closing_balance=row[" closing_balance "].replace(",", ""),
            business_profile=2,
            status="completed",
            created_on=date.today(),
            updated_on=date.today()
        )
        daily_summaries.append(daily_summary)

# Bulk create the DailySummary entries
DailySummary.objects.bulk_create(daily_summaries)
