from rest_framework.routers import DefaultRouter
from apps.text import views

router = DefaultRouter()

router.register(r'tag', views.TagViewset, basename='tag')


text_urlpatterns = router.urls