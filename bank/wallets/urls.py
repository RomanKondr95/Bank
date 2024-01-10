from django.urls import path, include
from .views import (
    WalletsDetailView,
    WalletsListView,
    UserTransactionsView,
    WalletTransactionsView,
    TransactionDetailView,
)

# вот это нужно будет уточнить у ментора. Видимо очень важен порядок маршрутов. По какому принципу? Я рассставлял методом проб и ошибок
urlpatterns = [
    path("auth/", include("rest_framework.urls")),
    # по этому маршруту не работает POST запрос
    path(
        "wallets/transactions/",
        UserTransactionsView.as_view(),
        name="user-transactions",
    ),
    path("wallets/", WalletsListView.as_view(), name="wallets-list"),
    path("wallets/<str:name>/", WalletsDetailView.as_view(), name="wallets-detail"),
    path(
        "wallets/transactions/<int:id>/",
        TransactionDetailView.as_view(),
        name="transaction-detail",
    ),
    path(
        "wallets/transactions/<str:wallet_name>/",
        WalletTransactionsView.as_view(),
        name="wallet-transactions",
    ),
]
