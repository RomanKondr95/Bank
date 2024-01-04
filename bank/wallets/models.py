import secrets
import string
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError


class Wallets(models.Model):
    VISA = "Visa"
    MASTERCARD = "Mastercard"
    TYPE_CHOICES = [
        (VISA, "Visa"),
        (MASTERCARD, "Mastercard"),
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

    def save(self, *args, **kwargs):
        user_wallets_count = Wallets.objects.filter(user=self.user).count()
        if not self.name:
            self.name = self.generate_unique_name()
        if not self.pk:
            if not self.balance:
                if self.currency in [self.USD, self.EUR]:
                    self.balance = 3
                elif self.currency == self.RUB:
                    self.balance = 100
            if user_wallets_count >= 5:
                raise ValidationError("User cannot create more than 5 wallets")
        super().save(*args, **kwargs)

