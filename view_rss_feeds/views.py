from django.views.generic import ListView

from store_rss_feeds.models import RSSSource, RSSFeedArticle


class ArticleListView(ListView):
    paginate_by = 10
    model = RSSFeedArticle
    template_name = 'articles.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Viewing Articles stored locally'
        context['publishers'] = RSSSource.objects.all()
        return context


class ArticleListByPublisherIdView(ListView):
    paginate_by = 10
    template_name = 'articles-by-source.html'

    def get_queryset(self):
        self.rss_source = RSSSource.objects.filter(id=self.publisher_id).get()
        return RSSFeedArticle.objects.filter(rss_source=self.rss_source)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Viewing Articles for {self.rss_source.id}'
        return context

    @property
    def publisher_id(self):
        return self.kwargs['publisher_id']
