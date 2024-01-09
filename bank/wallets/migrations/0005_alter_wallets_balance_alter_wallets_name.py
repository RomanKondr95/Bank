# Generated by Django 5.0.1 on 2024-01-06 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallets', '0004_alter_wallets_balance_alter_wallets_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallets',
            name='balance',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='wallets',
            name='name',
            field=models.CharField(max_length=8, unique=True),
        ),
    ]
