from decimal import Decimal
from typing import Union
from rest_framework import serializers
from .models import Wallets, Transactions
from .services import WalletService, TransactionService


class WalletSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()

    def get_name(self, obj: Union[dict, Wallets]) -> str:
        if isinstance(obj, dict):
            return obj.get("name", WalletService.generate_unique_name())
        return obj.name if obj.name else WalletService.generate_unique_name()

    def get_balance(self, obj: Union[dict, Wallets]) -> Decimal:
        wallet_currency = obj.get("currency") if isinstance(obj, dict) else obj.currency
        return str(WalletService.calculate_initial_balance(wallet_currency))

    class Meta:
        model = Wallets
        exclude = ("user",)


class TransactionSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source="sender.name", read_only=True)
    receiver = serializers.CharField(source="receiver.name", read_only=True)

    class Meta:
        model = Transactions
        fields = [
            "id",
            "sender",
            "receiver",
            "transfer_amount",
            "comission",
            "status",
            "timestamp",
        ]


class TransactionCreateSerializer(serializers.ModelSerializer):
    sender = serializers.CharField()
    receiver = serializers.CharField()
    transfer_amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Transactions
        fields = ["sender", "receiver", "transfer_amount"]

    def save(self, **kwargs) -> Union[Transactions, None]:
        sender_name = self.validated_data["sender"]
        receiver_name = self.validated_data["receiver"]

        transaction = TransactionService.create_transaction(
            sender_name=sender_name,
            receiver_name=receiver_name,
            transfer_amount=self.validated_data["transfer_amount"],
        )

        return transaction
