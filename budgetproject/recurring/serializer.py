from rest_framework import serializers
from .models import RecurringTransaction

class RecurringListSerializer(serializers.ModelSerializer):
    # user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    account_name = serializers.CharField(source="account.name", read_only=True)
    category_type = serializers.CharField(source="category.type", read_only=True)
    display_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = RecurringTransaction
        fields = ["id", "display_name", "account", "account_name", "category", "category_type", "currency", "is_active", "last_run"]


class RecurringDetailSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(required=False)
    # user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    account_name = serializers.CharField(source="account.name", read_only=True)
    category_type = serializers.CharField(source="category.type", read_only=True)
    display_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = RecurringTransaction
        fields = [
            "id",
            "display_name", 
            "account",
            "account_name",
            "category",
            "category_type",
            "amount",
            "currency",
            "description",
            "is_active",
            "frequency",
            "start_date",
            "last_run",
            "created",
            "updated"
        ]
