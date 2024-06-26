# Generated by Django 4.1.13 on 2024-06-25 06:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('biztrackapp', '0041_user_is_employee_alter_user_is_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bank',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='expensetype',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='receipttype',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='transactionmode',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_employee',
            field=models.BooleanField(default=True),
        ),
    ]
