from rest_framework import viewsets
from apps.text.models import Tag
from apps.text.serializers import TagSerializer
from rest_framework.permissions import IsAuthenticated


class TagViewset(viewsets.ModelViewSet):
    queryset = Tag.active_objects.active()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 
