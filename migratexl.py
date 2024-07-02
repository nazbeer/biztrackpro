import os
import django
import pandas as pd
import random
import string

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biztrackpro.settings')
django.setup()

from biztrackapp.models import DailySummary

file_path = 'Migration file latest.xlsx'
df = pd.read_excel(file_path)

def generate_random_id():
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"DS_{random_string}"

for index, row in df.iterrows():
    daily_summary = DailySummary(
        date=row['date'],
        opening_balance=row.get('opening_balance', None),
        daily_summary_id=generate_random_id(),
        cash_sale=row.get('cash_sale', None),
        credit_sale=row.get('credit_sale', None),
        card_sale=row.get('card_sale', None),
        sales=row.get('sales', None),
        credit_collection=row.get('credit_collection', None),
        miscellaneous_income=row.get('miscellaneous_income', None),
        purchase=row.get('purchase', None),
        supplier_payment=row.get('supplier_payment', None),
        expense=row.get('expense', None),
        withdrawal=row.get('withdrawal', None),
        bank_deposit=row.get('bank_deposit', None),
        closing_balance=row.get('closing_balance', None),
        business_profile='2', 
        status=row['status'],
        created_on=row.get('created_on', None),
        updated_on=row.get('updated_on', None)
    )
    daily_summary.save()

print("Data uploaded successfully.")
