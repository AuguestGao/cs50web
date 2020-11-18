from django.shortcuts import render

from . import util

#class NewEntryForm(forms.Form):
 #   entry = forms.CharField(label="new entry")


def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


#def entry(request):
 #   if request.method