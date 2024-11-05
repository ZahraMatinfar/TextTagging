from rest_framework import serializers
from apps.dataset.models import Dataset, Category
from apps.text.serializers import TextSerializer
from django.db.models import Count, OuterRef, Subquery, Value
from django.db.models.functions import Coalesce
from apps.text.models import Tag


class CategorySerializer(serializers.ModelSerializer):
    tag_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'tag_count', 'dataset']
        extra_kwargs = {
            "dataset": {"write_only": True},
        }


class DatasetListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ('id', 'name', 'description')


class DatasetSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()
    texts = serializers.SerializerMethodField()

    class Meta:
        model = Dataset
        fields = '__all__'
        read_only_fields = ['is_active']

    
    def get_categories(self, obj):
        # Fetch categories with tag counts annotated for each dataset
        categories_with_counts = obj.categories.annotate(
            tag_count=Coalesce(
                Subquery(
                    Tag.objects.filter(
                        text__dataset=obj,
                        category=OuterRef('pk')
                    ).values('category').annotate(count=Count('id')).values('count')
                ),
                Value(0)  # Default to 0 if no tags are found
            )
        )
        return CategorySerializer(categories_with_counts, many=True).data

    def get_texts(self, obj):
        request = self.context.get("request")
        texts = obj.texts.filter(is_active=True)

        # Apply search filter if query parameter 'search' is present
        search_query = request.query_params.get('search')
        if search_query:
            texts = texts.filter(content__icontains=search_query)

        return TextSerializer(texts, many=True).data