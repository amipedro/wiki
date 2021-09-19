from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from . import util
import markdown2 as mk

from django.http import HttpResponse


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

        # List of webpage entries
        entries = util.list_entries()

        # Check if queried word is listed in entries list
        if query.lower() in (entry.lower() for entry in entries):
            # Send user to page in case word is found
            return HttpResponseRedirect(f"wiki/{query}")
        else:
            # TODO
            print("Not found :(")
            return HttpResponseRedirect(f"search")