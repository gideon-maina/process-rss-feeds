import csv
import tempfile

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction, IntegrityError
from .models import RSSSource, RSSFeedArticle
from .forms import RSSSourcesFileForm


def index(request):
    context = {"title": "Welcome to RSS processor"}
    return render(request, "index.html", context=context)


def store_feeds(request):
    form = RSSSourcesFileForm()
    context = {"title": "Store RSS Feeds", "form": form}

    if request.method == 'POST':
        form = RSSSourcesFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Call the Process sources in the background
            source_file = request.FILES['source_file']
            stored_sources_count, duplicate_count = store_rss_feeds(
                source_file)
            # Redirect to the same page with success message
            mess = f"Saved {stored_sources_count} sources, Skipped {duplicate_count} duplicate sources"
            messages.add_message(request, messages.INFO, mess)
            return redirect("store_feeds")
        else:
            context = {"title": "Store RSS Feeds", "form": form}
            return render(request, 'store-feeds.html', context=context)
    else:
        form = RSSSourcesFileForm()
        return render(request, 'store-feeds.html', context=context)


def store_rss_feeds(request_source_file):
    file_field_names = ['publisher', 'url']
    temp_file = tempfile.NamedTemporaryFile(delete=True)

    with open(temp_file.name, 'wb') as tmp_file:
        for chunk in request_source_file.chunks():
            tmp_file.write(chunk)

    saved_sources_count = 0
    duplicate_count = 0
    with open(temp_file.name, 'r') as tmp_file:
        sources = csv.DictReader(tmp_file, fieldnames=file_field_names)
        next(sources, None)
        # Start DB transaction here
        for s in sources:
            try:
                url = s['url']
                publisher = s['publisher']
                source = RSSSource(
                    publisher=publisher,
                    url=url,
                )
                source.save()
                saved_sources_count += 1
            except IntegrityError:
                duplicate_count += 1
            except Exception:
                print(f"Error saving {s}")

    temp_file.close()
    return saved_sources_count, duplicate_count
