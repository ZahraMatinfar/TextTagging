from rest_framework.routers import DefaultRouter
from apps.text import views

router = DefaultRouter()

router.register(r'tag', views.TagViewset, basename='tag')
router.register(r'text', views.TextViewset, basename='text')
router.register(r'(?P<dataset_id>[^/.]+)/search', views.TextSearchViewSet, basename='search')


text_urlpatterns = router.urls