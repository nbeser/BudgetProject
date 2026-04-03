from rest_framework import generics
from recurring.models import RecurringTransaction
from recurring.serializer import RecurringListSerializer, RecurringDetailSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import ValidationError
from django.utils import timezone


class RecurringListView(generics.ListAPIView):
    """Admin: Recurring Transactions"""
    queryset = RecurringTransaction.objects.all()
    serializer_class = RecurringListSerializer
    permission_classes = [IsAdminUser]

class RecurringByUser(generics.ListCreateAPIView):
    """User: Recurring Transaction"""
    serializer_class = RecurringDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = RecurringTransaction.objects.filter(user=self.request.user)
        return queryset.order_by("-created")
    
    def perform_create(self, serializer):
        category = serializer.validated_data.get("category")
        start_date = serializer.validated_data.get("start_date")
        
        if not start_date:
            start_date = timezone.now()

        if category and category.is_parent:
            raise ValidationError({"category": "Parent category cannot be used for (recurring)transactions."})


        serializer.save(
            user=self.request.user,
            start_date = start_date
        )
    
    