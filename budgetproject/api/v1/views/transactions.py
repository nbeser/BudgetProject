from rest_framework import generics
from transaction.serializer import TransactionListSerializer, TransactionDetailSerializer
from transaction.models import Transaction
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import ValidationError
from django.utils import timezone




class TransactionListView(generics.ListAPIView):
    """Admin: Transactions"""
    queryset = Transaction.objects.all()
    serializer_class = TransactionListSerializer
    permission_classes = [IsAdminUser]

class TransactionByUser(generics.ListCreateAPIView):
    """User: Transaction list/create"""
    serializer_class = TransactionDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user)
    
        start = self.request.query_params.get("start")
        end = self.request.query_params.get("end")
        account = self.request.query_params.get("account")
        category = self.request.query_params.get("category")
        category_type = self.request.query_params.get("type")

        if start:
            queryset = queryset.filter(transaction_date__gte=start)
        if end:
            queryset = queryset.filter(transaction_date__lte=end)
        if account:
            queryset = queryset.filter(account_id=account)
        if category:
            queryset = queryset.filter(category_id=category)
        if category_type:
            queryset = queryset.filter(category__type=category_type)
        return queryset.order_by("-transaction_date")
    
    def perform_create(self, serializer):
        transaction_date = serializer.validated_data.get("transaction_date")
        category = serializer.validated_data.get("category")
        if not transaction_date:
            transaction_date = timezone.now()
        if category.is_parent:
            raise ValidationError({"category": "Parent category cannot be used for transactions."})

        serializer.save(
            user=self.request.user,
            transaction_date=transaction_date
        )


    



class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionDetailSerializer
    permission_classes = [IsAuthenticated]    

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
    

    def perform_update(self, serializer):
        category = serializer.validated_data.get("category")

        if category and category.is_parent:
            raise ValidationError({
                "category": "Parent category cannot be used for transactions."
            })

        serializer.save()