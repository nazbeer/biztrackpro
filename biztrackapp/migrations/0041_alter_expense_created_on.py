# Generated by Django 5.0.6 on 2024-07-02 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biztrackapp', '0040_alter_expense_created_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='created_on',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]