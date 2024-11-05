from django_filters import rest_framework as filters

from apps.dataset.models import Dataset

class DatasetFilter(filters.FilterSet):
    search = filters.CharFilter(field_name='texts__content', lookup_expr='icontains')

    class Meta:
        model = Dataset
        fields = ['search']