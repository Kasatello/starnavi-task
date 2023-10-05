from rest_framework import routers
from django.urls import path, include
from .views import PostViewSet, PostLikeViewSet, AnalyticsViewSet

router = routers.DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")
router.register(r"activity", AnalyticsViewSet, basename="post-analytics")

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "post"
