from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.urls import reverse
from django import forms

from . import util
import random, re

import markdown2


class NewPageForm(forms.Form):
    entry = forms.CharField(widget=forms.TextInput(
        attrs={
            'label':'Title',
            'class':'form-control col-lg-6',
            'name':'title'}))
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
            entry = form.cleaned_data["entry"]
            content = form.cleaned_data["content"]

            if entry in util.list_entries():
                massage = 'Entry ' + entry
                return render(request, "encyclopedia/error.html", {
                    "msg":massage
                })
            else:
                util.save_entry(entry, content)
                return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={'entry': entry}))

        else:
            return render(request, "encyclopedia/new.html", {
                "form": form
            })
    # if request.method == "GET"
    return render(request, "encyclopedia/new.html", {
        "form": NewPageForm()})# empty form


def randompage(request):
    choices = util.list_entries()
    choice = random.choice(choices)
    return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={
        "entry": choice}))


def edit(request, entry):
    if request.method == "GET":
        content = util.get_entry(entry)
        form = NewPageForm(initial={
        "entry": entry,
        "content":content})
        return render(request, "encyclopedia/edit.html", {
                "form": form,
                "entry": entry})
    else:
        form = NewPageForm(request.POST)
        if form.is_valid():
            entry = form.cleaned_data["entry"]
            content = form.cleaned_data["content"]
            util.save_entry(entry, content)
            return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={'entry': entry}))        
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form})            
