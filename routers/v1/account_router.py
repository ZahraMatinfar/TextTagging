from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.account.views import RegisterViewSet, LoginViewSet

router = DefaultRouter()
router.register(r'register', RegisterViewSet, basename='register')
router.register(r'login', LoginViewSet, basename='login')

account_urlpatterns = router.urls
