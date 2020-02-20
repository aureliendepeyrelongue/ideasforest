from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView)
from .models import Post, Comment, Like
from .forms import CommentForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator
from .constants import POSTS_PER_PAGE
from .utils import get_posts_and_likes

# Create your views here.
def post_list_view(request):
    posts = Post.objects.all().order_by('-date_posted')
    list_ = []
    for post in posts:
        likes_number = post.get_likes().count()
        already_liked = False

        if request.user.is_authenticated:
            already_liked = Like.objects.filter(post=post,author=request.user).exists()

        list_.append({
            'post' : post,
            'likes_number' : likes_number,
            'already_liked' : already_liked
        })
    
    paginator = Paginator(list_, POSTS_PER_PAGE)
    page = request.GET.get('page')
    list_page = paginator.get_page(page)
    is_paginated = len(list_) > POSTS_PER_PAGE

    return render(request, 'blog/home.html',{
    'home_active': 'active',
    'list' : list_page,
    'is_paginated' : is_paginated
    })

def user_post_list_view(request,pk):
    user = get_object_or_404(User,id=pk)
    posts = Post.objects.filter(author=user).order_by('-date_posted')
    list_ = []
    
    for post in posts:
        likes_number = post.get_likes().count()
        already_liked = False

        if request.user.is_authenticated:
            already_liked = Like.objects.filter(post=post,author=request.user).exists()

        list_.append({
            'post' : post,
            'likes_number' : likes_number,
            'already_liked' : already_liked
        })
    
    paginator = Paginator(list_, POSTS_PER_PAGE)
    page = request.GET.get('page')
    list_page = paginator.get_page(page)
    is_paginated = len(list_) > POSTS_PER_PAGE
    return render(request, 'blog/user_posts.html',{
    'home_active': 'active',
    'list' : list_page,
    'is_paginated' : is_paginated
    })

def search_results_list_view(request):
    list_ = []
    queryset = []
    queries = request.GET.get('q').split(" ")
    for q in queries:
        posts = Post.objects.filter(
            Q(title__icontains=q) | Q(content__icontains=q)
        ).distinct()
        for post in posts:
            found = False
            for existing in queryset:
                if existing == post:
                    found = True
            if found == False:
                queryset.append(post)
    
    for post in queryset:
        likes_number = post.get_likes().count()
        already_liked = False
        if request.user.is_authenticated:
            already_liked = Like.objects.filter(post=post,author=request.user).exists()

        list_.append({
            'post' : post,
            'likes_number' : likes_number,
            'already_liked' : already_liked
        })
    
    paginator = Paginator(list_, POSTS_PER_PAGE)
    page = request.GET.get('page')
    list_page = paginator.get_page(page)
    is_paginated = len(list_) > POSTS_PER_PAGE
    return render(request, 'blog/search_results.html',{
    'home_active': 'active',
    'list' : list_page,
    'is_paginated' : is_paginated
    })

def ajax_like(request,pk):
	if request.method == 'GET' and request.is_ajax() and request.user.is_authenticated:
         post = get_object_or_404(Post, id=pk)
         try:
             like = Like.objects.get(post=post,author=request.user)
             like.delete()
             liked = False
         except ObjectDoesNotExist:
             Like.objects.create(post=post,author=request.user)
             liked = True
         return JsonResponse({'success':True, 'liked' : liked}, status=200)
	return JsonResponse({'success':False}, status=400)
# Create your views here.

def post_detail_view(request,pk):
    context = {}
    post = get_object_or_404(Post, id=pk)
    comments = Comment.objects.filter(post=post)
    already_liked = False
    if request.user.is_authenticated:
        already_liked = Like.objects.filter(post=post,author=request.user).exists()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        form.instance.author = request.user
        form.instance.post = post
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('content')
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html',{
    'about_active': 'active',
    'comments' : comments,
    'post' : post,
    'form' : form,
    'likes_number' : post.get_likes().count(),
    'already_liked' : already_liked
    })


class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
class PostCreateView(LoginRequiredMixin,CreateView):
    model= Post
    fields = ['title', 'content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context['post_create_active'] = 'active'
        return context

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model= Post
    fields = ['title', 'content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

def about(request):
      context = {}
      context['about_active'] = 'active'
      return render(request, 'blog/about.html',context)
# Create your views here.
