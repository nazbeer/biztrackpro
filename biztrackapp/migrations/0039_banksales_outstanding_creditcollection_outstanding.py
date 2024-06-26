# Generated by Django 4.1.13 on 2024-06-21 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biztrackapp', '0038_alter_allbank_created_on_alter_bank_created_on_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='banksales',
            name='outstanding',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='creditcollection',
            name='outstanding',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
