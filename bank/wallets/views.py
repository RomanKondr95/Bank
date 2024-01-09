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


class WalletsListView(ListCreateAPIView):
    queryset = Wallets.objects.all()
    serializer_class = WalletSerializer
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        return Wallets.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WalletsDetailView(RetrieveDestroyAPIView):
    queryset = Wallets.objects.all()
    serializer_class = WalletSerializer
    lookup_field = "name"


class UserTransactionsView(ListCreateAPIView):
    serializer_class = TransactionCreateSerializer

    def get_queryset(self):
        user = self.request.user
        return Transactions.objects.filter(
            Q(sender__user=user) | Q(receiver__user=user)
        )

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TransactionSerializer
        elif self.request.method == "POST":
            return TransactionCreateSerializer
        return TransactionSerializer

    # def post(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def perform_create(self, serializer):
    #     serializer.save()



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


# class TransactionCreateView(ListCreateAPIView):
#     queryset = Transactions.objects.all()
#     serializer_class = TransactionSerializer

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#     def perform_create(self, serializer):
#         serializer.save()
