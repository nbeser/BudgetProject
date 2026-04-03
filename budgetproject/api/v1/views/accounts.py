from rest_framework import generics
from account.serializer import AccountListSerializer, AccountDetailSerializer
from account.models import Account

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import ValidationError


class AccountListView(generics.ListAPIView):
    """Admin: Accounts"""
    queryset = Account.objects.all()
    serializer_class = AccountListSerializer
    permission_classes = [IsAdminUser]


class AccountsByUser(generics.ListCreateAPIView):
    serializer_class = AccountDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Account.objects.filter(user=self.request.user)
        return queryset.order_by("-created")
    
    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )


class AccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AccountDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)
    
