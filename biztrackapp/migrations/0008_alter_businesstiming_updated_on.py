# Generated by Django 4.1.13 on 2024-05-29 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biztrackapp', '0007_bankdeposits_daily_summary_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businesstiming',
            name='updated_on',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
