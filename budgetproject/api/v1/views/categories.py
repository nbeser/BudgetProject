from rest_framework import generics
from category.serializer import CategoryListSerializer
from category.models import Category
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import ValidationError


class CategoryListView(generics.ListAPIView):
    """Admin: Categories"""
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    permission_classes = [IsAdminUser]
    

# class CategoryListByUser(generics.ListAPIView):
#     """User: Category/ies by users"""
#     def get_queryset(self):
#         return Category.objects.filter(user=self.request.user)
#     serializer_class = CategoryListSerializer
#     permission_classes = [IsAuthenticated]


# class CreateCategory(generics.CreateAPIView):
#     serializer_class = CategoryListSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         name = serializer.validated_data.get("name")
#         if Category.objects.filter(user=self.request.user, name=name).exists():
#             raise ValidationError({"message": "You already have this category."})
#         serializer.save(user=self.request.user)


class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategoryListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        name = serializer.validated_data.get("name")
        if Category.objects.filter(user=self.request.user, name=name).exists():
            raise ValidationError({"message": "You already have this category."})
        serializer.save(user=self.request.user)