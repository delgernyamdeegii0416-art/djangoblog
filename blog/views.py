from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Post, Category
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import PostForm
from django.contrib.auth import login
from django.views.generic.edit import CreateView
from .forms import PostForm, RegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


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
    return render(request, 'blog/home.html', {'title': 'This is the Djangblog Homepage.'})

def about(request):
    return render(request,'blog/about.html', {'team': 'This is the Djangoblog team.'})   

def contact(request):
    return render(request,'blog/contact.html',{'content': 'i`m Deegii.'})     

def post_list(request):
    posts = Post.objects.filter(status="published").order_by("-created_at")
    categories = Category.objects.all()
    paginator = Paginator(posts, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "blog/post_list.html",
        {
            "page_obj": page_obj,
            "categories": categories,
        }
    )
class PostCreateView(CreateView):
    model = Post
    template_name = "blog/post_form.html"
    form_class = PostForm

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"slug": self.object.slug}) 

class PostUpdateView(UpdateView):
    model = Post
    template_name = "blog/post_form.html"
    form_class = PostForm

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"slug": self.object.slug})            

class PostDeleteView(DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("home")

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