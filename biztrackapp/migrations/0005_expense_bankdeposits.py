# Generated by Django 4.1.13 on 2024-05-25 13:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('biztrackapp', '0004_supplierpayments'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cheque_no', models.CharField(blank=True, max_length=255, null=True)),
                ('invoice_no', models.CharField(max_length=255)),
                ('cheque_date', models.DateField()),
                ('business_profile', models.CharField(max_length=255, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biztrackapp.bank')),
                ('expense_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biztrackapp.expensetype')),
                ('mode_of_transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biztrackapp.transactionmode')),
            ],
        ),
        migrations.CreateModel(
            name='BankDeposits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('deposit_date', models.DateField()),
                ('cheque_date', models.DateField()),
                ('cheque_no', models.CharField(max_length=255)),
                ('business_profile', models.CharField(max_length=255, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deposits_as_bank', to='biztrackapp.bank')),
                ('bank_deposit_bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deposits_as_bank_deposit', to='biztrackapp.bank')),
                ('mode_of_transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biztrackapp.transactionmode')),
            ],
        ),
    ]
