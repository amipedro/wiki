from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from . import util
import markdown2 as mk

from django.http import HttpResponse
from django.urls import reverse


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    # Get page content
    content = util.get_entry(entry)

    if content is not None:
        # Converts from markdown to HTML
        content = mk.markdown(content)

        # Render page
        return render(request, "encyclopedia/entry.html", {
            "title": entry,
            "text": content
        })

    else:
        return render(request, "encyclopedia/error.html", {
            "name": entry
        })

def search(request):
    if request.method == "GET":
        # Get query from searchbar
        query = request.GET.get('q')
        query = query.lower()

        # List of webpage entries
        entries = util.list_entries()

        # Check if queried word is listed in entries list
        if query in (entry.lower() for entry in entries):
            # Send user to page in case word is found
            return HttpResponseRedirect(f"wiki/{query}")

        # Check if query is part of any of listed entries
        else:
            # Create a list of strings based on a substring
            subs = []
            for entry in entries:
                if query in entry.lower():
                    subs.append(entry)

            # If subs list is populated, render a page with possible found words
            if subs:
                return render(request, "encyclopedia/search.html", {
                    "substrings": subs,
                    "query": query
                })

            # If the list is not populated, render a page informing that anything was found.
            else:
                not_found = "not found"
                return render(request, "encyclopedia/search.html", {
                    "not_found": not_found,
                    "query": query
                })