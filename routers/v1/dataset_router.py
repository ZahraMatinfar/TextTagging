# datasets/urls.py
from rest_framework.routers import DefaultRouter
from apps.dataset import views

router = DefaultRouter()
router.register(r'', views.DatasetViewSet, basename='dataset')


dataset_urlpatterns = router.urls
