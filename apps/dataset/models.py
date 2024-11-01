from django.db import models
from core.models.base import BaseModel
from django.utils.translation import gettext_lazy as _


class Dataset(BaseModel):
    name = models.CharField(_("name"), max_length=255, unique=True)
    description = models.TextField(_("description"), blank=True)

    class Meta:
        verbose_name = _("dataset")
        verbose_name_plural = _("datasets")

    def __str__(self):
        return self.name


class Category(BaseModel):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name="categories", verbose_name=_("dataset"))
    name = models.CharField(_("name"), max_length=255)

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return f"{self.name} ({'Active' if self.is_active else 'Inactive'})"

