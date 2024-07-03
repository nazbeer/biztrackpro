import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biztrackpro.settings')
django.setup()

from biztrackapp.models import ExpenseType



expense_types = [
    "PETROL",
    "FOOD",
    "SALARY",
    "VEHICLE EXP",
    "REPAIRE & MAINTANENCE",
    "CHARITY",
    "CARRY BAG",
    "TELEPHONE",
    "SHOP EXP",
    "GOVT EXP",
    "TELEPHONE CHARGE",
    "AADC",
    "VISA EXP",
    "GENERAL EXP",
    "INAUGRATION PROGRAM",
    "GAS",
    "PARKING",
    "PEST CONTROL",
    "ROOM RENT",
    "TRAVEL EXP",
    "OPENING ADJUSTMENT"
]

for expense_type in expense_types:
    new_expense_type = ExpenseType(
        name=expense_type,
        business_profile='2',
        status=True,
        created_on=datetime.now()
    )
    new_expense_type.save()

print("Expense types added successfully.")
