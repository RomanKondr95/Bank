import pytest
from django.urls import reverse
from .snapshots_utils import snapshot_check


@pytest.mark.django_db
def test_get_wallet_list(api_client, wallet, another_wallet):
    snapshot_check(api_client, "/wallets/", "get_wallet_list_response")


# Проверка кошелька по имени
@pytest.mark.django_db
def test_get_detail_wallet(api_client, wallet):
    snapshot_check(api_client, "/wallets/AW2J6U5F/", "get_detail_wallet_response")


# Тест получения списка транзакций
@pytest.mark.django_db
def test_user_transactions_view(api_client, wallet, another_wallet, transaction):
    snapshot_check(
        api_client, reverse("user-transactions"), "get_transaction_list_response"
    )


# Тест получения транзакции по имени кошелька
@pytest.mark.django_db
def test_wallets_transaction(api_client, transaction, wallet, another_wallet):
    snapshot_check(
        api_client,
        reverse("wallet-transactions", kwargs={"wallet_name": "BWX2J7U5"}),
        "get_transaction_name_detail_response",
    )


# Тест получения транзакции по айдишнику
@pytest.mark.django_db
def test_id_transaction(api_client, wallet, another_wallet, transaction):
    snapshot_check(
        api_client,
        reverse("transaction-detail", kwargs={"id": transaction.id}),
        "get_transaction_id_detail_response",
    )
