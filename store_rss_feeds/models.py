from django.db import models


class RSSSource(models.Model):
    """Model to store the RSS publishers and the metadata"""
    id = models.AutoField(primary_key=True)
    publisher = models.CharField(max_length=200)
    url = models.URLField(unique=True)
    topic = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=1000)
    last_build_date = models.DateTimeField(null=True)
    last_refresh = models.DateTimeField(auto_now=True, )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True, )


class RSSFeedArticle(models.Model):
    id = models.AutoField(primary_key=True)
    rss_source = models.ForeignKey(RSSSource, on_delete=models.CASCADE)
    link = models.URLField()
    title = models.CharField(max_length=50)
    slug = models.SlugField()
    guid = models.CharField(max_length=500)
    pubdate = models.DateTimeField()
    description = models.CharField(max_length=1000)
    last_refresh = models.DateTimeField(auto_now=True, )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True, )
