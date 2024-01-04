from django.contrib import admin
from .models import Wallets


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