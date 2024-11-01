# datasets/urls.py
from rest_framework.routers import DefaultRouter
from apps.dataset import views

router = DefaultRouter()

router.register(r'dataset', views.DatasetViewSet, basename='dataset')
router.register(r'category', views.CategoryViewSet, basename='category')


dataset_urlpatterns = router.urls
