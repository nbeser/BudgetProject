from rest_framework import generics
from category.serializer import CategoryListSerializer
from category.models import Category
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class CategoryListView(generics.ListAPIView):
    """Admin: Categories"""
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    permission_classes = [IsAdminUser]
    

class CategoryListByUser(generics.ListAPIView):
    """User: Category/ies by users"""
    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)
    serializer_class = CategoryListSerializer
    permission_classes = [IsAuthenticated]
    