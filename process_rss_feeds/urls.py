"""process_rss_feeds URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from store_rss_feeds import views as store_rss_views
from refresh_rss_feeds import views as refresh_rss_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', store_rss_views.index, name='index'),
    path('store-rss-feeds/store',
         store_rss_views.store_feeds,
         name='store_feeds'),
    path('view-rss-feeds/', include('view_rss_feeds.urls')),
    path('refresh-rss-feeds/refresh',
         refresh_rss_views.refresh_feeds,
         name="refresh_feeds"),
]
