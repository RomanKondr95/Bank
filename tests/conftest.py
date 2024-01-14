import pytest
from rest_framework.test import APIClient
from wallets.factories import TransactionFactory, UserFactory, WalletFactory


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(api_client):
    user = UserFactory()
    api_client.force_authenticate(user=user)
    return user

@pytest.fixture
def wallet(user):
    wallet = WalletFactory.create(user=user, name="AW2J6U5F")
    return wallet

@pytest.fixture
def another_wallet(user):
    wallet = WalletFactory.create(user=user, name="BWX2J7U5")
    return wallet

@pytest.fixture
def transaction(wallet, another_wallet):
    transaction = TransactionFactory.create(
        sender=wallet,
        receiver=another_wallet,
        transfer_amount=2,
    )
    return transaction
