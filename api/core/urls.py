from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaperViewset

router = DefaultRouter()
router.register(r'paper', PaperViewset)

urlpatterns = [
    path("", include(router.urls))
]