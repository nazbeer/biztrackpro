# Generated by Django 5.0.6 on 2024-07-16 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biztrackapp', '0045_transactionmode_transaction_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailySummaryRemark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('daily_summary_id', models.CharField(blank=True, max_length=100, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('closing_balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('business_profile', models.CharField(max_length=255, null=True)),
                ('created_on', models.DateField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
