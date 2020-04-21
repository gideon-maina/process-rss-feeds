from django.urls import path
from .views import ArticleListView, ArticleListByPublisherIdView

urlpatterns = [
    path('', ArticleListView.as_view(), name='articles-list'),
    path('<publisher_id>/',
         ArticleListByPublisherIdView.as_view(),
         name='articles-list-by-source-id')
]
