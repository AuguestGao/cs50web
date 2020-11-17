from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # "" = default route, name is optnioanl, better to include for reference
    path("ag", views.ag, name="ag"),
    path("<str:name>", views.greet, name="greet")
]