from rest_framework import viewsets
from apps.dataset.filters import DatasetFilter
from apps.dataset.models import Dataset, Category
from apps.dataset.serializers import DatasetSerializer, DatasetListSerializer, CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from core.api.permissions import IsAdminOrReadOnly


class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.active_objects.active().prefetch_related('categories', 'texts', 'categories__tags')
    serializer_class = DatasetSerializer
    filterset_class = DatasetFilter
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return DatasetListSerializer
        return DatasetSerializer
    
    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user

        if user.is_admin:
           return qs
        else:
            return qs.filter(users=user)
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='search',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Search texts within the dataset by content'
            ),
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.active_objects.active()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]