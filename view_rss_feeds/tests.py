import datetime
import os

from django.test import TestCase, Client

from .views import ArticleListView
from store_rss_feeds.models import RSSSource, RSSFeedArticle


class ArticlesListTest(TestCase):
    def setUp(self):
        self.current_path = os.path.dirname(os.path.realpath(__file__))
        self.sample_file = os.path.join(self.current_path,
                                        'sample-upload-test.csv')
        self.url = '/view-rss-feeds/'
        self.client = Client()
        # Create dummy articles
        source = RSSSource.objects.create(publisher='bbc',
                                          url='http://dummy-url.com.xml')
        # Create 12 dummy articles so that pagination activates
        for i in range(12):
            article = RSSFeedArticle.objects.create(
                rss_source=source,
                title=f"title {i}",
                description="Description",
                link="https://hello-dummy.article.com",
                guid="234",
                pubdate=datetime.datetime.now())

    def test_articles_viewing(self):
        r = self.client.get(self.url)
        self.assertEqual(200, r.status_code)

    def test_pagination_items(self):
        r = self.client.get(self.url)
        self.assertTrue('is_paginated' in r.context)
        self.assertTrue(r.context['is_paginated'] == True)
        self.assertTrue(len(r.context['object_list']) == 10)
