# Generated by Django 4.1.13 on 2024-06-06 04:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('biztrackapp', '0020_withdrawal_cheque_date_withdrawal_cheque_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankdeposits',
            name='bank',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deposits_as_bank', to='biztrackapp.bank'),
        ),
        migrations.AlterField(
            model_name='banksales',
            name='bank',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='biztrackapp.bank'),
        ),
        migrations.AlterField(
            model_name='creditcollection',
            name='bank',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='biztrackapp.bank'),
        ),
        migrations.AlterField(
            model_name='dailysummary',
            name='bank_deposit',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='dailysummary',
            name='card_sale',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='dailysummary',
            name='cash_sale',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='dailysummary',
            name='closing_balance',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='dailysummary',
            name='credit_collection',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='dailysummary',
            name='credit_sale',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='dailysummary',
            name='expense',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='dailysummary',
            name='miscellaneous_income',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='dailysummary',
            name='opening_balance',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='dailysummary',
            name='purchase',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='dailysummary',
            name='sales',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='dailysummary',
            name='supplier_payment',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='expense',
            name='bank',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='biztrackapp.bank'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='cheque_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='miscellaneousincome',
            name='bank',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='biztrackapp.bank'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='bank',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='biztrackapp.bank'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='invoice_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='invoice_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='invoice_no',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='opening_outstanding',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='supplierpayments',
            name='bank',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='biztrackapp.bank'),
        ),
        migrations.AlterField(
            model_name='supplierpayments',
            name='opening_outstanding',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]