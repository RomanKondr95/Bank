# Generated by Django 5.0.1 on 2024-01-04 19:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=8, unique=True)),
                ('type', models.CharField(choices=[('Visa', 'Visa'), ('Mastercard', 'Mastercard')], max_length=10)),
                ('currency', models.CharField(choices=[('USD', 'USD'), ('EUR', 'EUR'), ('RUB', 'RUB')], max_length=3)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
