from django.urls import path
from .import views

urlpatterns = [
  path('', views.NewsListView.as_view(), name='item_list'),
  path('detail/<int:pk>/', views.NewsDetailView.as_view(), name='item_detail'),
]
