from django.contrib import admin
from .models import Wallets, Transactions
from .services import WalletService, TransactionService

@admin.register(Wallets)
class WalletAdmin(admin.ModelAdmin):
    fields = ("type", "currency", "user")

    def save_model(self, request, obj, form, change):
        WalletService.save_wallet(obj, change)
        super().save_model(request, obj, form, change)

@admin.register(Transactions)
class TransactionAdmin(admin.ModelAdmin):
    fields = ("sender", "receiver", "transfer_amount")

    def save_model(self, request, obj, form, change):
        TransactionService.save_transaction(obj, change)
        super().save_model(request, obj, form, change)

