from typing import Union
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveDestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
)
from .models import Wallets, Transactions
from .serializers import (
    TransactionCreateSerializer,
    WalletSerializer,
    TransactionSerializer,
)
from rest_framework.authentication import SessionAuthentication
from django.db.models import Q
from .services import WalletService, TransactionService


class WalletsListView(ListCreateAPIView):
    serializer_class = WalletSerializer
    authentication_classes = [SessionAuthentication]

    def get_queryset(self) -> list[Wallets]:
        return WalletService.get_user_wallets(self.request.user)

    def perform_create(self, serializer: WalletSerializer):
        WalletService.create_wallet(
            serializer.validated_data["type"],
            serializer.validated_data["currency"],
            self.request.user,
        )


class WalletsDetailView(RetrieveDestroyAPIView):
    queryset = Wallets.objects.all()
    serializer_class = WalletSerializer
    lookup_field = "name"


class UserTransactionsView(ListCreateAPIView):
    serializer_class = TransactionCreateSerializer

    def get_queryset(self) -> list[Transactions]:
        return TransactionService.get_user_transactions(self.request.user)

    def get_serializer_class(
        self,
    ) -> Union[TransactionSerializer, TransactionCreateSerializer]:
        if self.request.method == "GET":
            return TransactionSerializer
        elif self.request.method == "POST":
            return TransactionCreateSerializer
        return TransactionSerializer

    def perform_create(self, serializer: TransactionCreateSerializer):
        serializer.save()


class WalletTransactionsView(ListAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self) -> list[Transactions]:
        wallet_name = self.kwargs["wallet_name"]
        return Transactions.objects.filter(
            Q(sender__name=wallet_name) | Q(receiver__name=wallet_name)
        )


class TransactionDetailView(RetrieveAPIView):
    queryset = Transactions.objects.all()
    serializer_class = TransactionSerializer
    lookup_field = "id"
