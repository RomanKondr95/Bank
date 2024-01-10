from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Wallets(models.Model):
    VISA = "Visa"
    MASTERCARD = "Mastercard"
    TYPE_CHOICES = [
        (VISA, "visa"),
        (MASTERCARD, "mastercard"),
    ]
    USD = "USD"
    EUR = "EUR"
    RUB = "RUB"
    CURRENCY_CHOICES = [
        (USD, "USD"),
        (EUR, "EUR"),
        (RUB, "RUB"),
    ]
    name = models.CharField(max_length=8, unique=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Transactions(models.Model):
    sender = models.ForeignKey(
        Wallets, related_name="sent_transaction", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        Wallets, related_name="received_transaction", on_delete=models.CASCADE
    )
    transfer_amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    comission = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, default="PAID")
    timestamp = models.DateTimeField(auto_now_add=True)
