from django.contrib import admin

from apps.dataset.models import Dataset, Category, DatasetReport
from core.admin.base import BaseAdmin

class CategoryInline(admin.TabularInline):
    model = Category
    extra =0

@admin.register(Dataset)
class DatasetAdmin(BaseAdmin):
    inlines = [CategoryInline]
    list_display = ("name",)


@admin.register(DatasetReport)
class DatasetReportAdmin(BaseAdmin):
    list_display = ("dataset_name",)
    search_fields = ("dataset__name",)