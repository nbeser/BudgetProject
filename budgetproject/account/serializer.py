from rest_framework import serializers
from .models import Account

class AccountListSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model = Account
        fields = ["user", "name", "account_type", "is_active"]


class AccountDetailSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    opening_balance = serializers.DecimalField(max_digits=12, decimal_places=2, write_only=True, required=False)
    balance = serializers.ReadOnlyField()
    class Meta:
        model = Account
        fields = [
            "id",
            "name",
            "user",
            "account_type",
            "currency",
            "created",
            "updated",
            "is_active",
            "balance",
            "opening_balance"
        ]
    
    def create(self, validated_data):
        opening_balance = validated_data.pop("opening_balance", None)
        account = Account(**validated_data)
        account._opening_balance = opening_balance
        account.save()
        return account
