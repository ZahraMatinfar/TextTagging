from rest_framework import viewsets, mixins
from apps.text.models import Tag, Text
from apps.text.serializers import TagSerializer, TextSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from core.api.permissions import IsAdminOrReadOnly


class TextSearchViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = TextSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['content']
    lookup_field = 'dataset_id'

    def get_queryset(self):
        dataset_id = self.kwargs['dataset_id']
        return Text.objects.filter(dataset_id=dataset_id, dataset__users=self.request.user)

class TextViewset(viewsets.ModelViewSet):
    queryset = Text.active_objects.active()
    serializer_class = TextSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    

class TagViewset(viewsets.ModelViewSet):
    queryset = Tag.active_objects.active()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 
