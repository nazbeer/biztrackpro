# Generated by Django 5.0.6 on 2024-07-12 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biztrackapp', '0043_alter_bankdeposits_created_on_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditcollection',
            name='created_on',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]