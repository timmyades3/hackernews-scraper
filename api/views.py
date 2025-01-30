from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework import status
from scraper.models import Comment, News
from .serializers import NewsItemSerializer, NewsListSerializer, NewsDetailSerializer,CommentSerializer
from django.db.models import Q
from django.utils import timezone
from django.http import Http404


class NewsListAPIView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsListSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description="Search term", type=openapi.TYPE_STRING),
            openapi.Parameter('type', openapi.IN_QUERY, description="Type of item", type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        """
        Return the filtered queryset based on search and type filters.
        """
        queryset = News.objects.all()

        # Filter by search term using Q objects to combine the conditions with OR
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(text__icontains=search_query)
            )

        # Filter by type
        type_filter = self.request.GET.get('type', '')
        if type_filter:
            queryset = queryset.filter(type=type_filter)

        return queryset


class NewsItemCreateView(generics.CreateAPIView):
    serializer_class = NewsItemSerializer

    def perform_create(self, serializer):
        serializer.save()


class NewsItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsDetailSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.is_posted:
            return Response({"detail": "You can only update news that are posted."}, status=status.HTTP_403_FORBIDDEN)
        instance.date_created = timezone.now()
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.is_posted:
            return Response({"detail": "You can only delete news that are posted."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
    
class CommentListAPIView(generics.ListAPIView):
    serializer_class = CommentSerializer

    @swagger_auto_schema(
        tags=['Comments'],
        manual_parameters=[
            openapi.Parameter('text', openapi.IN_QUERY, description="Comment text", type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        """
        Return the filtered queryset based on item_id and text filters.
        """
        item_id = self.request.GET.get('item_id')
        text_query = self.request.GET.get('text', '')

        filters = {}
        if item_id:
            filters['news_id'] = item_id
        if text_query:
            filters['text__icontains'] = text_query

        return Comment.objects.filter(**filters)


class CommentDetailView(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "comment_id"  # Ensure we query by comment_id instead of pk

    @swagger_auto_schema(tags=['Comments'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self, *args, **kwargs):
        comment_id = self.kwargs.get('comment_id')
        try:
            return Comment.objects.get(comment_id=comment_id)
        except Comment.DoesNotExist:
            raise Http404("Comment not found")
