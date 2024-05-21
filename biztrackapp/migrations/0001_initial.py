# Generated by Django 5.0.6 on 2024-05-21 12:19

import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=64, null=True)),
                ('license_number', models.CharField(max_length=255)),
                ('license_expiration', models.DateField(null=True)),
                ('license_upload', models.FileField(upload_to='licenses')),
                ('shop_phone_number', models.CharField(max_length=25)),
                ('vat_percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('vat_number', models.CharField(max_length=255)),
                ('vat_submission_date_1', models.DateField(null=True)),
                ('vat_submission_date_2', models.DateField(null=True)),
                ('vat_submission_date_3', models.DateField(null=True)),
                ('vat_certificate_upload', models.FileField(upload_to='vat_certificates')),
                ('address', models.TextField()),
                ('license_expiration_reminder_days', models.PositiveIntegerField(verbose_name='License Expiration Reminder (days)')),
                ('vat_submission_date_reminder_days', models.PositiveIntegerField(verbose_name='VAT Submission Date Reminder (days)')),
                ('employee_visa_expiration_reminder_days', models.PositiveIntegerField(verbose_name='Employee Visa Expiration Reminder (days)')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Shop Name')),
                ('license_number', models.CharField(max_length=50, unique=True)),
                ('num_users', models.PositiveIntegerField(verbose_name='Number of Users')),
                ('vat_remainder', models.BooleanField(default=True, verbose_name='VAT Reminder')),
                ('employee_transaction_window', models.BooleanField(default=True)),
                ('license_expiration_reminder', models.BooleanField(default=True, verbose_name='License Expiration Reminder')),
                ('employee_visa_expiration_reminder', models.BooleanField(default=True, verbose_name='Employee Visa Expiration Reminder')),
                ('employee_passport_expiration_reminder', models.BooleanField(default=True, verbose_name='Employee Passport Expiration Reminder')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=100, unique=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('country_code', models.CharField(max_length=10)),
                ('phone_number', models.CharField(max_length=20)),
                ('is_admin', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ShopAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biztrackapp.shop')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
