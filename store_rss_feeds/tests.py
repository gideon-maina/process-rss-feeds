import os

from django.test import TestCase, Client
from store_rss_feeds.models import RSSSource
from store_rss_feeds.forms import RSSSourcesFileForm


class TestRSSSourcesStorage(TestCase):
    def setUp(self):
        self.current_path = os.path.dirname(os.path.realpath(__file__))
        self.sample_file = os.path.join(self.current_path,
                                        'sample-upload-test.csv')
        self.store_url = '/store-rss-feeds/store'
        self.client = Client()

    def test_view_index_page(self):
        r = self.client.get('')
        self.assertEqual(200, r.status_code)

    def test_source_file_upload(self):
        with open(self.sample_file) as fh:
            params = {'source_file': fh}
            r = self.client.post(self.store_url, params)
            self.assertEqual(r.status_code, 302)

    def test_create_sources_from_upload(self):
        expected_created_rss_source = RSSSource(
            publisher='cnn',
            url='http://rss.cnn.com/rss/edition_motorsport.rss')

        with open(self.sample_file) as fh:
            params = {'source_file': fh}
            r = self.client.post(self.store_url, params)
            self.assertEqual(302, r.status_code)
            # Fetch all the current sources
            source = RSSSource.objects.first()
            self.assertEqual(expected_created_rss_source.url.strip(),
                             source.url.strip())
