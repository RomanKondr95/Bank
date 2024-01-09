import logging
from rest_framework import serializers
from .models import Wallets, Transactions


class WalletSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()

    def get_name(self, obj):
        if obj.name:
            return obj.name
        return Wallets.generate_unique_name()

    def get_balance(self, obj):
        if obj.balance:
            return obj.balance
        return Wallets.calculate_initial_balance(obj)

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


# class TransactionCreateSerializer(serializers.ModelSerializer):
#     sender = serializers.CharField(source="sender.name")
#     receiver = serializers.CharField(source="receiver.name")
    

#     class Meta:
#         model = Transactions
#         fields = [
#             "sender",
#             "receiver",
#             "transfer_amount",
#         ]
        
class TransactionCreateSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source="sender.name")
    receiver = serializers.CharField(source="receiver.name")

    class Meta:
        model = Transactions
        fields = [
            "sender",
            "receiver",
            "transfer_amount",
        ]

    def create(self, validated_data):
        sender_name = validated_data["sender"]
        receiver_name = validated_data["receiver"]


        sender_wallet, _ = Wallets.objects.get_or_create(user=self.context['request'].user,name=sender_name)
        receiver_wallet, _ = Wallets.objects.get_or_create(user=self.context['request'].user,name=receiver_name)


        transaction = Transactions.objects.create(
            sender=sender_wallet,
            receiver=receiver_wallet,
            transfer_amount=validated_data["transfer_amount"],
            status="PAID"
        )

        return transaction