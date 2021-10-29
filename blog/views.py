from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

from blog.forms import NewCommentForm
from .models import Post, Comment
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

"""
posts = [
    {
        'author': 'Roy',
        'title': 'Blog post 1',
        'content': 'First post content',
        'date_posted': 'August 29, 2021'
    },
    {
        'author': 'Mee',
        'title': 'Blog post 2',
        'content': 'First post content Mee',
        'date_posted': 'August 30, 2021'
    }
]
"""
"""
def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)
"""
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html example blog/post_list.html
    context_object_name = 'posts'
    ordering = ['-date_posted'] # newest post is at the top
    paginate_by = 5

class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/user_posts.html' 
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        #comments_connected = Comment.objects.filter(post = self.get_object()).order_by('-date_posted')
        #context['comments'] = comments_connected
        context['comment_form'] = NewCommentForm(instance=self.request.user)

        return context
    
    def post(self, request, *args, **kwargs):
        new_comment = Comment(content=request.POST.get('content'), 
                            author=self.request.user,
                            post=self.get_object())
        #print(f"The host name is {self.request.get_host()}")
        new_comment.save()
        return self.get(self, request, *args, **kwargs)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

"""
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        form.instance.author = self.request.user
        return super().form_valid(form)
"""

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def test(req):
    a = req.get_host()
    return HttpResponse(f"The host is {a}")
