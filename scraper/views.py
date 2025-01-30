from django.views.generic import ListView
from .models import News, Comment
from django.views.generic import DetailView
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render


class NewsListView(ListView):
    model = News
    template_name = 'news_list.html'
    context_object_name = 'news_items'
    paginate_by = 10

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        type_query = self.request.GET.get('type', '')
        queryset = News.objects.all()

        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        if type_query:
            queryset = queryset.filter(type=type_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['news_items'] = page_obj
        return context


class NewsDetailView(DetailView):
    model = News
    template_name = 'news_detail.html'
    context_object_name = 'details'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news = self.get_object()
        context['comments'] = Comment.objects.filter(parent=news.item_id)  # Ensure this is correct
        return context

