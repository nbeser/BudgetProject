from rest_framework import serializers
from .models import Transaction


class TransactionListSerializer(serializers.ModelSerializer):
    # user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    category_type = serializers.CharField(source="category.type", read_only=True)
    display_name = serializers.CharField(source='user.name', read_only=True)
    class Meta:
        model = Transaction
        fields = ["id", "display_name", "account", "category", "category_type", "amount", "currency"]


class TransactionDetailSerializer(serializers.ModelSerializer):
    # user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    transaction_date = serializers.DateTimeField(required=False)
    display_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = Transaction
        fields = ["id", "display_name", "account", "category", "amount", "currency", "description", "transaction_date"]