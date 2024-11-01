from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.dataset.models import Dataset
from core.costants import choices
from django.utils.translation import gettext_lazy as _


from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    datasets = models.ManyToManyField(Dataset, related_name="users", blank=True, verbose_name=_("datasets"))
    role = models.SmallIntegerField(_("role"), choices=choices.ROLE_CHOICES, default=choices.OPERATOR_ROLE)

    def __str__(self):
        return f"{self.username} (Role: {self.get_role_display()})"

