"""
V1 api routers
"""
from django.urls import (
    include,
    path,
)
from .account_router import account_urlpatterns
from .dataset_router import dataset_urlpatterns
from .text_router import text_urlpatterns

urlpatterns = [
     path("account/", include(account_urlpatterns)),
     path('dataset/', include(dataset_urlpatterns)),
     path('text/', include(text_urlpatterns)),
]