# Generated by Django 4.1.13 on 2024-06-06 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biztrackapp', '0023_alter_banksales_bank_alter_creditcollection_bank_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailysummary',
            name='withdrawal',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
