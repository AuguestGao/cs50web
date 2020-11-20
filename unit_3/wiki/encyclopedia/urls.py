from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki", views.search, name="search"),
    path("wiki/<str:entry>", views.wiki, name="entry")
]