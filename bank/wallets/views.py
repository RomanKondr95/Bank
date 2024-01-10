import logging
from venv import logger
from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveDestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
)
from .models import Wallets, Transactions
from .serializers import (
    TransactionCreateSerializer,
    WalletSerializer,
    TransactionSerializer,
)
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from wallets import serializers
from .services import WalletService, TransactionService


class WalletsListView(ListCreateAPIView):
    serializer_class = WalletSerializer
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        return WalletService.get_user_wallets(self.request.user)

    def perform_create(self, serializer):
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

    def get_queryset(self):
        return TransactionService.get_user_transactions(self.request.user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TransactionSerializer
        elif self.request.method == "POST":
            return TransactionCreateSerializer
        return TransactionSerializer

    def perform_create(self, serializer):
        serializer.save()


class WalletTransactionsView(ListAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        wallet_name = self.kwargs["wallet_name"]
        return Transactions.objects.filter(
            Q(sender__name=wallet_name) | Q(receiver__name=wallet_name)
        )


class TransactionDetailView(RetrieveAPIView):
    queryset = Transactions.objects.all()
    serializer_class = TransactionSerializer
    lookup_field = "id"
