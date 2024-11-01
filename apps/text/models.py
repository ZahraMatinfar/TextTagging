from django.db import models
from django.contrib.auth import get_user_model
from apps.dataset.models import Category, Dataset
from core.models.base import BaseModel
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class Text(BaseModel):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name="texts", verbose_name=_("dataset"))
    content = models.TextField(_("content"))

    class Meta:
        verbose_name = _("text")
        verbose_name_plural = _("texts")

    def __str__(self):
        return f"{self.content}"

    
class Tag(BaseModel):
    text = models.ForeignKey(Text, on_delete=models.CASCADE, related_name="tags", verbose_name=_("text"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="tags", verbose_name=_("category"))
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=_("user"), related_name="tags")

    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'text', 'category'],
                name='unique_user_text_category_tag'
            )
        ]

    def __str__(self):
        return f"Tagging of {self.text} with {self.category}"

