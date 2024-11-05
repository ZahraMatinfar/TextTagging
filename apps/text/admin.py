from django.contrib import admin
from apps.text.models import Text, Tag
from core.admin.base import BaseAdmin

@admin.register(Text)
class TextAdmin(BaseAdmin):
    search_fields = ("content", )
    list_filter = ("dataset", )


@admin.register(Tag)
class TagAdmin(BaseAdmin):
    search_fields = ("text__content", )
    list_filter = ("category", "user")