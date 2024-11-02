from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.account import views
router = DefaultRouter()

router.register(r"auth", views.AuthViewSet, basename="auth")

account_urlpatterns = router.urls
