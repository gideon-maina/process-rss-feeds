# Generated by Django 3.0.5 on 2020-04-20 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RSSSource',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('publisher', models.CharField(max_length=200)),
                ('url', models.URLField()),
                ('topic', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=1000)),
                ('last_build_date', models.DateField()),
                ('last_refresh', models.DateField(auto_now=True)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_modified', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='RSSFeedArticle',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('link', models.URLField()),
                ('title', models.CharField(max_length=50)),
                ('slug', models.SlugField()),
                ('guid', models.CharField(max_length=500)),
                ('pubdate', models.DateField()),
                ('description', models.CharField(max_length=1000)),
                ('last_refresh', models.DateField(auto_now=True)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_modified', models.DateField(auto_now=True)),
                ('rss_source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store_rss_feeds.RSSSource')),
            ],
        ),
    ]