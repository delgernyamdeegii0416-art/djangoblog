
from django.urls import path
from .views import (
    post_list, post_detail, MyPostsView, PostCreateView, PostUpdateView, PostDeleteView, RegisterView, about,
    contact,
)

urlpatterns = [
    path("", post_list, name="home"),
    path("my-posts/", MyPostsView.as_view(), name="my_posts"),
    path("register/", RegisterView.as_view(), name="register"),
    path("posts/new/", PostCreateView.as_view(), name="post_create"),
    path("posts/<slug:slug>/edit/", PostUpdateView.as_view(), name="post_edit"),
    path("posts/<slug:slug>/delete/", PostDeleteView.as_view(), name="post_delete"),
    path("posts/<slug:slug>/", post_detail, name="post_detail"),
    path("about/", about, name="about"),
    path("contact/", contact, name="contact"),
]