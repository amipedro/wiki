from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from . import util
import markdown2 as mk

from django.http import HttpResponse
from django.urls import reverse
import random as rd

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

def create(request):

    # Read form for a Post request
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')

        # List of entries
        entries = util.list_entries()
        
        # Conditional sintax for posting information
        # Shows a error message in case the entry already exists.
        if title.lower() in (entry.lower() for entry in entries):
            
            message = "The content you tried to save already exists."

            return render(request, "encyclopedia/create.html", {
                "message": message,
                "title": title
            })
        # Allows the user to save content to website "database"
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(f"wiki/{title}")

    else:
        return render(request, "encyclopedia/create.html")

def edit(request):

    return render(request, "edit.html")


# Redirect to a random page
def random(request):

    rand = rd.choice(util.list_entries())

    return HttpResponseRedirect(f"wiki/{rand}")