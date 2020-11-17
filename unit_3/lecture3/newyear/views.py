
import datetime
from django.shortcuts import render

# Create your views here.
def index(request):
    #logic here
    now = datetime.datetime.now()
    return render(request, "newyear/index.html", {
        "newyear": now.month == 1 and now.day == 1
    })
