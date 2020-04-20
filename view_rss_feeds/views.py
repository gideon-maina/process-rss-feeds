from django.shortcuts import render
from django.views.generic import ListView

from store_rss_feeds.models import RSSSource, RSSFeedArticle


class ArticleListView(ListView):
    paginate_by = 10
    model = RSSFeedArticle
    template_name = 'articles.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Viewing Articles stored locally'
        return context
