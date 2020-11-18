from django.shortcuts import render
from django.http import HttpResponse

from . import util
import markdown2
#class NewEntryForm(forms.Form):
 #   entry = forms.CharField(label="new entry")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    entry_md = util.get_entry(title)
    if entry_md:
        #use markdown2 to convert .md to .html
        entry_html = markdown2.markdown(entry_md)
        return render(request, "encyclopedia/entry.html", {
            "entry_html": entry_html,
            "title": title
        })
    return render(request, "encyclopedia/error.html", {
            "title": title
        })