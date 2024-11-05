from django.contrib import admin
from core.admin.mixins import EditInlineButton


class BaseAdmin(
    EditInlineButton, 
    admin.ModelAdmin
):
    pass