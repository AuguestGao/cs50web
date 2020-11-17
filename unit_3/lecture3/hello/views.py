from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
# view = what uses see
def index(request):
    return render(request, "hello/index.html") # temple name in ""

def ag(request):
    return HttpResponse("Hello, Auguest!")


def greet(request, name):
    """
    function take takes name and greet the person
    """
    # argument goes after html
    return render(request, "hello/greet.html", {
        "name": name.capitalize()
    })