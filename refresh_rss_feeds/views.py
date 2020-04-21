import datetime
from xml.etree import ElementTree

import dateparser
import requests
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render
from store_rss_feeds.models import RSSSource, RSSFeedArticle


def refresh_feeds(request):
    sources = RSSSource.objects.all()
    refreshed_sources_count = sources.count()
    new_articles = 0
    session = requests.Session()

    with transaction.atomic():
        for source in sources:
            # Get latest stored article for this source
            latest_article = RSSFeedArticle.objects.filter(
                rss_source=source).order_by('pubdate').last()
            # Fetch it's contents
            r = session.get(source.url)
            xml_data = ElementTree.fromstring(r.content)
            for item in xml_data.findall('channel/item'):
                item_data = item.getchildren()
                for item_attr in item_data:
                    if item_attr.tag == 'title':
                        title = item_attr.text
                    elif item_attr.tag == 'link':
                        link = item_attr.text
                    elif item_attr.tag == 'description':
                        description = item_attr.text
                    elif item_attr.tag == 'guid':
                        guid = item_attr.text
                    elif item_attr.tag == 'pubDate':
                        pub_date = dateparser.parse(item_attr.text)
                # Save the article
                article = RSSFeedArticle(rss_source=source,
                                         title=title,
                                         description=description,
                                         link=link,
                                         guid=guid,
                                         pubdate=pub_date)
                if latest_article:
                    if article.pubdate > latest_article.pubdate:
                        new_articles += 1
                        article.save()
                else:
                    # Save it this is the first run
                    new_articles += 1
                    article.save()
            # Update last refresh date for the sources
            RSSSource.objects.filter(id=source.id).update(
                last_refresh=datetime.datetime.now())
            # Update the last build date for the sources
            last_build_date = xml_data.find('channel/lastBuildDate')
            last_build_date = dateparser.parse(last_build_date.text)
            RSSSource.objects.filter(id=source.id).update(
                last_build_date=last_build_date)

    context = {'title': "Refreshing Feed Articles"}
    messages.add_message(
        request, messages.INFO,
        f"Refreshed {refreshed_sources_count} sources adding {new_articles} articles to local db."
    )
    return render(request, 'refreshed.html', context=context)
