from decimal import Decimal
import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from wallets.factories import TransactionFactory, UserFactory, WalletFactory
from rest_framework.test import APIClient
from wallets.models import Transactions, Wallets


@pytest.fixture
def api_client():
    return APIClient()


# Создание юзера и кошелька. Вынес в отдельную фикстуру
# Два кошелька нужны для тестов транзакций
@pytest.fixture
def wallet_creation(api_client):
    user = UserFactory()
    api_client.force_authenticate(user=user)
    wallet1 = WalletFactory.create(name="AW2J6U5F")
    wallet2 = WalletFactory.create(name="BWX2J7U5")
    return {"api_client": api_client, "wallet1": wallet1, "wallet2": wallet2}


# Проверка списка кошельков
# Снапшоты пока не стал использовать. Там какая-то проблема с импортом
@pytest.mark.django_db
def test_get_wallet_list(wallet_creation):
    api_client = wallet_creation["api_client"]
    wallet = wallet_creation["wallet1"]
    response = api_client.get("/wallets/")
    assert response.status_code == 200
    assert Wallets.objects.count() == 2
    if wallet.currency == "RUB":
        assert wallet.balance == Decimal(100)
    elif wallet.currency in ["EUR", "USD"]:
        assert wallet.balance == Decimal(3)
    assert wallet.name == "AW2J6U5F"


# Проверка кошелька по имени
@pytest.mark.django_db
def test_get_detail_wallet(wallet_creation):
    api_client = wallet_creation["api_client"]

    response = api_client.get("/wallets/AW2J6U5F/")
    assert response.status_code == 200


# Фикстура для создания транзакции
@pytest.fixture
def create_transactions(api_client, wallet_creation):
    transaction = TransactionFactory.create(
        sender=wallet_creation["wallet1"],
        receiver=wallet_creation["wallet2"],
        transfer_amount=2,
    )

    return {
        "api_client": api_client,
        "transaction": transaction,
    }


# Тест получения списка транзакций
@pytest.mark.django_db
def test_user_transactions_view(create_transactions):
    api_client = create_transactions["api_client"]
    transaction = create_transactions["transaction"]
    response = api_client.get(reverse("user-transactions"))
    assert response.status_code == 200
    assert Transactions.objects.count() == 1
    assert transaction.id == 1
    assert transaction.sender.name == "AW2J6U5F"
    assert transaction.receiver.name == "BWX2J7U5"


# Тест получения транзакции по имени кошелька
@pytest.mark.django_db
def test_wallets_transaction(create_transactions):
    api_client = create_transactions["api_client"]
    response = api_client.get(
        reverse("wallet-transactions", kwargs={"wallet_name": "BWX2J7U5"})
    )
    assert response.status_code == 200


# Тест получения транзакции по айдишнику
@pytest.mark.django_db
def test_id_transaction(create_transactions):
    api_client = create_transactions["api_client"]
    transaction = create_transactions["transaction"]
    response = api_client.get(
        reverse("transaction-detail", kwargs={"id": transaction.id})
    )
    assert response.status_code == 200
