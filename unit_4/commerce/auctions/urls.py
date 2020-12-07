from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new, name="new"),
    path("listing/<int:id>", views.item, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"), 
    path("category", views.cate_index, name="cate_index"), 
    path("category/<str:name>", views.cate_name, name="category")
]
