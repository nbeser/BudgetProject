from rest_framework.authtoken.models import Token
from .models import Category

from rest_framework import serializers
# from django.contrib.auth import get_user_model
# User = get_user_model()

class CategoryListSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    class Meta:
        model = Category
        fields = ["id", "user", "name", "type", "is_active", "is_system", "is_parent"]

        extra_kwargs = {
            "user" : {"read_only" : True}
        }
