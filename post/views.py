from django.db.models import Count
from django.db.models.functions import TruncDate
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet

from user.models import CustomUser
from .models import Post, PostLike
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        if not isinstance(request.user, CustomUser):
            return Response({"error": "User is not authenticated"})

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostLikeViewSet(ViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=True, methods=["POST"])
    def like_post(self, request, pk=None):
        user = request.user
        post = get_object_or_404(Post, pk=pk)

        if PostLike.objects.filter(user=user, post=post).exists():
            return Response(
                {"detail": "You have already liked this post"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        PostLike.objects.create(user=user, post=post)
        return Response({"detail": "Post liked"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"])
    def unlike_post(self, request, pk=None):
        user = request.user
        post = get_object_or_404(Post, pk=pk)

        if not PostLike.objects.filter(user=user, post=post).exists():
            return Response(
                {"detail": "You have not liked this post"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        PostLike.objects.filter(user=user, post=post).delete()
        return Response(
            {"detail": "You have unliked this post"}, status=status.HTTP_200_OK
        )


class AnalyticsViewSet(ViewSet):
    def list(self, request):
        date_from = self.request.query_params.get("date_from")
        date_to = self.request.query_params.get("date_to")

        queryset = Post.objects.all()

        if date_from and date_to:
            queryset = queryset.filter(created_at__date__range=[date_from, date_to])

        queryset = (
            queryset.annotate(date=TruncDate("created_at"))
            .values("date")
            .annotate(likes_count=Count("likes"))
            .order_by("date")
        )

        analytics_data = list(queryset.values())

        response_data = {
            "analytics": [
                {
                    "date_from": item["date"].strftime("%Y-%m-%d"),
                    "likes_count": item["likes_count"],
                }
                for item in analytics_data
            ]
        }

        return Response(response_data)
