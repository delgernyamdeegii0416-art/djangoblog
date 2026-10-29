from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db import models
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Post, Category
from .forms import PostForm, RegisterForm


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    login_url = "login"
    success_url = reverse_lazy("home")

    def test_func(self):
        return self.get_object().author == self.request.user


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status="published")
    return render(request, "blog/post_detail.html", {"post": post})


def home(request):
    posts = Post.objects.filter(status="published").order_by("-created_at")

    # Category filter: /?category=<category name>
    selected_category = request.GET.get("category", "").strip()
    if selected_category:
        posts = posts.filter(category__name__iexact=selected_category).distinct()

    paginator = Paginator(posts, 6)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "blog/home.html", {
        "page_obj": page_obj,
        "categories": Category.objects.all(),
        "selected_category": selected_category,
        "title": "Home",
    })

def home(request):
    posts = Post.objects.filter(status="published").order_by("-created_at")

    selected_category = request.GET.get("category", "").strip()
    if selected_category:
        posts = posts.filter(category__name__iexact=selected_category).distinct()

    paginator = Paginator(posts, 6)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "blog/home.html", {
        "page_obj": page_obj,
        "categories": Category.objects.all(),
        "selected_category": selected_category,
        "title": "Home",
    })    


def about(request):
    return render(request, 'blog/about.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        body = request.POST.get("message", "").strip()

        if name and email and body:
            messages.success(request, "お問い合わせを送信しました。ありがとうございます！")
            return redirect("contact")

        messages.error(request, "すべての項目を入力してください。")
        return render(request, "blog/contact.html", {"values": request.POST})

    return render(request, "blog/contact.html")


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    paginate_by = 6

    def get_queryset(self):
        qs = Post.objects.filter(
            status="published"
        ).order_by("-created_at")

        category_slug = self.request.GET.get("category")

        if category_slug:
            qs = qs.filter(
                category__name__iexact=category_slug
            )

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


def custom_403(request, exception=None):
    return render(request, "blog/403.html", status=403)


def custom_404(request, exception):
    return render(request, "blog/404.html", status=404)


def custom_500(request):
    return render(request, "blog/500.html", status=500)


def test_500(request):
    raise Exception("Testing custom 500 page")


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "blog/register.html"
    success_url = "/"

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    login_url = "login"

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"slug": self.object.slug})


class MyPostsView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "blog/my_posts.html"
    paginate_by = 6
    login_url = "login"

    def get_queryset(self):
        return Post.objects.filter(
            author=self.request.user
        ).order_by("-created_at")


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    login_url = "login"

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post published successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"slug": self.object.slug})


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        post = Post.objects.filter(status="published")
        if self.request.user.is_authenticated:
            post = Post.objects.filter(
                models.Q(status="published") | models.Q(author=self.request.user)
            )
        return post