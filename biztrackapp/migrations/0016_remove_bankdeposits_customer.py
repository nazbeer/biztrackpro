# Generated by Django 4.1.13 on 2024-05-31 11:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('biztrackapp', '0015_alter_bankdeposits_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankdeposits',
            name='customer',
        ),
    ]
