# Generated by Django 4.1.13 on 2024-05-31 07:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('biztrackapp', '0012_businessprofile_opening_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankdeposits',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='biztrackapp.customer'),
        ),
        migrations.AlterField(
            model_name='bank',
            name='name',
            field=models.CharField(choices=[('FAB', 'FAB'), ('ADCB', 'ADCB'), ('AL MASRAF', 'AL MASRAF'), ('CBOD', 'CBOD'), ('Emirates NBD', 'Emirates NBD'), ('Mashreq', 'Mashreq'), ('Bank of Sharjah', 'Bank of Sharjah'), ('United Arab Bank', 'United Arab Bank'), ('Invest Bank', 'Invest Bank'), ('Rak Bank', 'Rak Bank'), ('CBI', 'CBI'), ('NBF', 'NBF'), ('NBQ', 'NBQ'), ('Dubai Islamic Bank', 'Dubai Islamic Bank'), ('Emirates Islamic Bank', 'Emirates Islamic Bank'), ('Sharjah Islamic Bank', 'Sharjah Islamic Bank'), ('ADIB', 'ADIB'), ('Al Hilal Bank', 'Al Hilal Bank'), ('Ajman Bank', 'Ajman Bank'), ('Arab Bank', 'Arab Bank'), ('Banque Misr', 'Banque Misr'), ('Bank of Baroda', 'Bank of Baroda'), ('Nilein Bank', 'Nilein Bank'), ('NBB', 'NBB'), ('BNP Paribas', 'BNP Paribas'), ('HSBC', 'HSBC'), ('AAIB', 'AAIB'), ('Al Khaliji', 'Al Khaliji'), ('ABK', 'ABK'), ('Barclays Bank', 'Barclays Bank'), ('HBL', 'HBL'), ('Habib Bank AG Zurich', 'Habib Bank AG Zurich'), ('Standard Chartered', 'Standard Chartered'), ('Citi Bank', 'Citi Bank'), ('Bank Saderat Iran', 'Bank Saderat Iran'), ('Bank Melli Iran', 'Bank Melli Iran'), ('Banque Banorient France', 'Banque Banorient France'), ('United Bank Limited', 'United Bank Limited'), ('Doha Bank', 'Doha Bank'), ('Samba Financial Group', 'Samba Financial Group'), ('Deutsche Bank', 'Deutsche Bank'), ('ICBC', 'ICBC'), ('NBK', 'NBK'), ('GIB', 'GIB'), ('Bank of China', 'Bank of China'), ('BOK', 'BOK'), ('Credit Agricole', 'Credit Agricole'), ('IDB', 'IDB')], max_length=255),
        ),
    ]