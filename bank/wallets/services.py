from decimal import Decimal
import secrets
import string

from django.forms import ValidationError
from .models import Wallets, Transactions, User
from django.db import transaction as tr
from django.db.models import Q


class WalletService:
    """
    Бизнес логика для кошельков

    """

    @staticmethod
    def get_user_wallets(user):
        return Wallets.objects.filter(user=user)

    @staticmethod
    def get_all_wallets():
        return Wallets.objects.all()

    @staticmethod
    def generate_unique_name():
        characters = string.ascii_uppercase + string.digits
        unique_name = "".join(secrets.choice(characters) for _ in range(8))
        return unique_name

    @staticmethod
    def calculate_initial_balance(currency):
        if currency in [Wallets.USD, Wallets.EUR]:
            return Decimal(3)
        elif currency == Wallets.RUB:
            return Decimal(100)

    @staticmethod
    def create_wallet(wallet_type, currency, user):
        wallet_type = Wallets.VISA if type == "Visa" else Wallets.MASTERCARD
        unique_name = WalletService.generate_unique_name()
        user_wallets_count = Wallets.objects.filter(user=user).count()
        if user_wallets_count >= 5:
            raise ValidationError("User cannot create more than 5 wallets")
        wallet = Wallets.objects.create(
            name=unique_name,
            type=wallet_type,
            currency=currency,
            balance=WalletService.calculate_initial_balance(currency),
            user=user,
        )

        wallet.save()
        return wallet


class TransactionService:
    """
    Бизнес логика для транзакций

    """

    @staticmethod
    def get_wallet_transactions(wallet_name):
        return Transactions.objects.filter(
            Q(sender__name=wallet_name) | Q(receiver__name=wallet_name)
        )

    @staticmethod
    def get_user_transactions(user):
        return Transactions.objects.filter(
            Q(sender__user=user) | Q(receiver__user=user)
        )

    @staticmethod
    def validate_currency(transaction):
        if transaction.sender.currency != transaction.receiver.currency:
            transaction.status = "FAILED"
            raise ValidationError(
                "Transaction allowed only for wallets with the same currency!"
            )

    @staticmethod
    def calculate_comission(transaction):
        if transaction.sender.user != transaction.receiver.user:
            transaction.comission = transaction.transfer_amount * Decimal(0.10)
        else:
            transaction.comission = Decimal(0.00)

    @staticmethod
    def validate_transfer(transaction):
        if (
            transaction.sender.balance
            < transaction.transfer_amount + transaction.comission
        ):
            transaction.status = "FAILED"
            raise ValidationError("Insufficient funds for the transaction!")

    @staticmethod
    def process_transaction(transaction: Transactions):
        transaction.sender.balance -= (
            transaction.transfer_amount + transaction.comission
        )
        transaction.receiver.balance += transaction.transfer_amount
        transaction.sender.save()
        transaction.receiver.save()

    @staticmethod
    def create_transaction(sender_name, receiver_name, transfer_amount):
        sender_wallet = Wallets.objects.get(name=sender_name)
        receiver_wallet = Wallets.objects.get(name=receiver_name)

        transaction = Transactions(
            sender=sender_wallet,
            receiver=receiver_wallet,
            transfer_amount=transfer_amount,
            status="PAID",
        )

        try:
            with tr.atomic():
                TransactionService.validate_currency(transaction)
                TransactionService.calculate_comission(transaction)
                TransactionService.validate_transfer(transaction)
                TransactionService.process_transaction(transaction)

                transaction.save()
                return transaction
        except ValidationError as e:
            return None
