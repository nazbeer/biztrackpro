# Generated by Django 4.1.13 on 2024-06-06 05:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('biztrackapp', '0022_allbank_alter_banksales_bank_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banksales',
            name='bank',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='biztrackapp.bank'),
        ),
        migrations.AlterField(
            model_name='creditcollection',
            name='bank',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='biztrackapp.bank'),
        ),
        migrations.AlterField(
            model_name='miscellaneousincome',
            name='bank',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='biztrackapp.bank'),
        ),
    ]
