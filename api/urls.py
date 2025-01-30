from django.urls import path
from .import views

urlpatterns = [
    path('item/', views.NewsListAPIView.as_view(), name='item_list'),
    path('item/create/', views.NewsItemCreateView.as_view(), name='create_item'),
    path('item/detail/<int:pk>/', views.NewsItemDetailView.as_view(), name='item_detail'),
    path('item/comment/', views.CommentListAPIView.as_view(), name='comment_list'),
    path("item/comment/detail/<int:comment_id>/", views.CommentDetailView.as_view(), name="comment-detail"),
]
