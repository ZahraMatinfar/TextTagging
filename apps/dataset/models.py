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
    

class DatasetReport(BaseModel):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='reports', verbose_name=_("dataset"))
    report_file = models.FileField(upload_to='reports/', verbose_name=_("reeport file"))


    class Meta:
        verbose_name = _("dataset report")
        verbose_name_plural = _("dataset reports")
        ordering = ["-created_time", "-updated_time"]

    def __str__(self):
        return f"Report for {self.dataset.name}"
    
    @property
    def dataset_name(self):
        return self.dataset.name
    dataset_name.fget.short_description = _("dataset name")   
