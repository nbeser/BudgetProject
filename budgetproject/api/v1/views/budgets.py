from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from budgets.models import Budget
from budgets.serializer import BudgetSerializer


class BudgetListCreateView(generics.ListCreateAPIView):
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        category = serializer.validated_data.get("category")
        account = serializer.validated_data.get("account")

        if category.type != "expense":
            raise ValidationError({
                "category": "Budget can only be created for expense categories."
            })

        if account and account.user != self.request.user:
            raise ValidationError({
                "account": "Account must belong to the same user."
            })

        serializer.save(user=self.request.user)



class BudgetDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)