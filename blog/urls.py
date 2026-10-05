from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),

    path("posts/", views.post_list, name="post_list"),
    path("post/<slug:slug>/", views.post_detail, name="post_detail"),

    path("posts/new/", views.PostCreateView.as_view(), name="post_create"),
    path("posts/<slug:slug>/edit/", views.PostUpdateView.as_view(), name="post_edit"),
    path("posts/<slug:slug>/delete/", views.PostDeleteView.as_view(), name="post_delete"),
]