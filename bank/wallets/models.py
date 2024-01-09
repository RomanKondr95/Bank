from decimal import Decimal
import secrets
import string
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.core.validators import MinValueValidator
from django.db import transaction


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

    def generate_unique_name(self):
        characters = string.ascii_uppercase + string.digits
        unique_name = "".join(secrets.choice(characters) for _ in range(8))
        return unique_name

    def calculate_initial_balance(self):
        if self.currency in [self.USD, self.EUR]:
            self.balance = 3
        elif self.currency == self.RUB:
            self.balance = 100

    def save(self, from_transaction=False, *args, **kwargs):
        user_wallets_count = Wallets.objects.filter(user=self.user).count()
        if not self.name:
            self.name = self.generate_unique_name()
        if not self.balance:
            self.calculate_initial_balance()
        if not from_transaction and user_wallets_count >= 5:
            raise ValidationError("User cannot create more than 5 wallets")
        super().save(*args, **kwargs)


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

    def save(self, *args, **kwargs):
        self.validate_currency()
        self.calculate_comission()

        self.validate_transfer()

        with transaction.atomic():
            self.process_transaction()
        super().save(*args, **kwargs)

    def validate_currency(self):
        if self.sender.currency != self.receiver.currency:
            self.status = "FAILED"
            raise ValidationError(
                "Transaction allowed only for wallets with the same currency!"
            )

    def calculate_comission(self):
        if self.sender.user != self.receiver.user:
            self.comission = self.transfer_amount * Decimal(0.10)
        else:
            self.comission = Decimal(0.00)

    def validate_transfer(self):
        if self.sender.balance < self.transfer_amount + self.comission:
            self.status = "FAILED"
            raise ValidationError("Insufficient funds for the transaction!")

    def process_transaction(self):
        self.sender.balance -= self.transfer_amount + self.comission
        self.receiver.balance += self.transfer_amount
        self.sender.save(from_transaction=True)
        self.receiver.save(from_transaction=True)
