# Generated by Django 5.0.6 on 2024-07-12 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biztrackapp', '0041_alter_expense_created_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankdeposits',
            name='created_on',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='banksales',
            name='created_on',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='creditcollection',
            name='created_on',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='dailysummary',
            name='created_on',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='expense',
            name='created_on',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='miscellaneousincome',
            name='created_on',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='created_on',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='supplierpayments',
            name='created_on',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='withdrawal',
            name='created_on',
            field=models.DateField(null=True),
        ),
    ]
