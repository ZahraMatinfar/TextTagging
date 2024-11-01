from rest_framework import viewsets
from apps.dataset.filters import DatasetFilter
from apps.dataset.models import Dataset, Category
from apps.dataset.serializers import DatasetSerializer, DatasetListSerializer, CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated


class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.active_objects.active().prefetch_related('categories', 'texts', 'categories__tags')
    serializer_class = DatasetSerializer
    filterset_class = DatasetFilter
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return DatasetListSerializer
        return DatasetSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.active_objects.active()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]