from decimal import Decimal
from factory import Faker, SubFactory, LazyAttribute, post_generation
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User
from .services import WalletService
from .models import Wallets, Transactions


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Faker("user_name")
    password = Faker("password")


class WalletFactory(DjangoModelFactory):
    class Meta:
        model = Wallets

    user = SubFactory(UserFactory)
    type = Faker("random_element", elements=["Visa", "MasterCard"])
    currency = Faker("random_element", elements=["RUB", "EUR", "USD"])
    balance = LazyAttribute(
        lambda obj: WalletService.calculate_initial_balance(obj.currency)
    )


class TransactionFactory(DjangoModelFactory):
    class Meta:
        model = Transactions
        skip_postgeneration_save = True

    sender = SubFactory(WalletFactory)
    receiver = SubFactory(WalletFactory)
    transfer_amount = 2
    status = "PAID"

    @post_generation
    def calculate_commission(obj, create, extracted, **kwargs):
        obj.commission = obj.transfer_amount * Decimal(0.10) if create else None
