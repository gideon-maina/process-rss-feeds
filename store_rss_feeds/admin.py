from django.contrib import admin

from .models import RSSSource, RSSFeedArticle

admin.site.register(RSSSource)
admin.site.register(RSSFeedArticle)
