from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.urls import reverse
from django import forms

from . import util

import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
    })

def wiki(request, entry):
    entry_md = util.get_entry(entry)

    if entry_md:
        #use markdown2 to convert .md to .html
        entry_html = markdown2.markdown(entry_md)
        return render(request, "encyclopedia/entries.html", {
            "entry_html": entry_html,
            "entry": entry
        })
    return render(request, "encyclopedia/error.html", {
            "entry": entry
        })

def search(request):
    entry = request.GET.get('entry', '')
    return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"entry": entry}))