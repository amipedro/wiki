from django.shortcuts import render

from . import util
import markdown2 as mk


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):

    content = util.get_entry(entry)

    if content is not None:
        content = mk.markdown(content)
        return render(request, "encyclopedia/entry.html", {
            "title": entry,
            "text": content
        })

    else:
        return render(request, "encyclopedia/error.html", {
            "name": entry
        })