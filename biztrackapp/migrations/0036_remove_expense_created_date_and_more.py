# Generated by Django 4.1.13 on 2024-06-12 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('biztrackapp', '0035_rename_create_date_expense_created_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expense',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='supplierpayments',
            name='create_date',
        ),
    ]