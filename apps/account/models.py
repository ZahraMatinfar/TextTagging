from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.dataset.models import Dataset
from django.utils.translation import gettext_lazy as _


from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    datasets = models.ManyToManyField(Dataset, related_name="users", blank=True, verbose_name=_("datasets"))

    def __str__(self):
        return f"{self.username}"
    
    @property
    def is_admin(self):
        return self.is_staff or self.is_superuser

