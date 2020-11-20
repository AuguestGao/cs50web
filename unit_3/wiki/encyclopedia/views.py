from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.urls import reverse
from django import forms

from . import util
import random

import markdown2


class NewPageForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(
        attrs={
            'label':'Title',
            'class':'form-control col-lg-6',
            'name':'title'
        }))
    content = forms.CharField(widget=forms.Textarea(
        attrs={
            'class':'form-control col-lg-6',
            'name':'content'
        }))
    
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
    massage = 'Title ' + entry + " not found"
    return render(request, "encyclopedia/error.html", {
            "msg": massage
        })

# search only redirects, to wiki, and wiki does the rendering
def search(request):
    entry = request.GET.get('entry', '')
    return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"entry": entry}))

def new(request): # new has request.method get and post
    if request.method == "POST":
        form = NewPageForm(request.POST) # get user's submit to form
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            if title in util.list_entries():
                massage = 'Title ' + title + " exists"
                return render(request, "encyclopedia/error.html", {
                    "msg":massage
                })
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={'entry': title}))

        else:
            return render(request, "encyclopedia/new.html", {
                "form": form
            })
    # if request.method == "GET"
    return render(request, "encyclopedia/new.html", {
        "form": NewPageForm() # empty form
    })


def randompage(request):
    choices = util.list_entries()
    choice = random.choice(choices)
    return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={
        "entry": choice}))
