# Generated by Django 4.1.13 on 2024-06-21 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('biztrackapp', '0039_banksales_outstanding_creditcollection_outstanding'),
    ]

    operations = [
        migrations.RenameField(
            model_name='creditcollection',
            old_name='outstanding',
            new_name='opening_outstanding',
        ),
    ]
