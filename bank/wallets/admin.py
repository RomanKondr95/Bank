from decimal import Decimal
from django.contrib import admin
from .models import Wallets, Transactions


@admin.register(Wallets)
class WalletAdmin(admin.ModelAdmin):
    fields = ("type", "currency", "user")

    def save_model(self, request, obj, form, change):
        if not change:
            if not obj.balance:
                if obj.currency in [obj.USD, obj.EUR]:
                    obj.balance = 3
                elif obj.currency == obj.RUB:
                    obj.balance = 100
            if not obj.name:
                obj.name = obj.generate_unique_name()

        super().save_model(request, obj, form, change)


# admin.site.register(Transactions)


@admin.register(Transactions)
class TransactionAdmin(admin.ModelAdmin):
    fields = ("sender", "receiver", "transfer_amount")

    def save_model(self, request, obj, form, change):
        if not change:
            if obj.sender.currency != obj.receiver.currency:
                obj.status = "FAILED"
                obj.save()
                return

            if obj.sender.user != obj.receiver.user:
                obj.commission = obj.transfer_amount * Decimal(0.10)
            else:
                obj.commission = Decimal(0.00)

        super().save_model(request, obj, form, change)
