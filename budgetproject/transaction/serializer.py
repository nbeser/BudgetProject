from rest_framework import serializers
from .models import Transaction

from account.models import Account
from category.models import Category


class TransactionListSerializer(serializers.ModelSerializer):
    # user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    category_type = serializers.CharField(source="category.type", read_only=True)
    display_name = serializers.CharField(source='user.name', read_only=True)
    class Meta:
        model = Transaction
        fields = ["id", "display_name", "account", "category", "category_type", "amount", "currency"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context["request"].user

        self.fields["account"].queryset = Account.objects.filter(user=user)
        self.fields["category"].queryset = Category.objects.filter(user=user, is_system=False)


class TransactionDetailSerializer(serializers.ModelSerializer):
    # user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    transaction_date = serializers.DateTimeField(required=False)
    display_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = Transaction
        fields = ["id", "display_name", "account", "category", "amount", "currency", "description", "transaction_date"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context["request"].user

        self.fields["account"].queryset = Account.objects.filter(user=user)
        self.fields["category"].queryset = Category.objects.filter(user=user, is_system=False)