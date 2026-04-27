from rest_framework import serializers
from .models import Budget


class BudgetSerializer(serializers.ModelSerializer):
    # user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    display_name = serializers.CharField(source='user.name', read_only=True)

    spent = serializers.SerializerMethodField()
    remaining = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Budget
        fields = [
            "id",
            "display_name",
            "category",
            "account",
            "amount",
            "start_date",
            "end_date",
            "is_active",
            "spent",
            "remaining",
            "progress",
        ]

    def get_spent(self, obj):
        return obj.spent_amount

    def get_remaining(self, obj):
        return obj.remaining_amount

    def get_progress(self, obj):
        return round(obj.progress_percentage, 2)