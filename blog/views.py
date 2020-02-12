from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView)
from .models import Post
from django.contrib.auth.models import User
from django.db.models import Q


# Create your views here.
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 16
    
    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['home_active'] = 'active'
        return context
    

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 16

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
        

class SearchPostListView(ListView):
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 16

    def get_queryset(self):
        queryset = []
        queries = self.request.GET.get('q').split(" ")
        
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
        
        return queryset

# Create your views here.
class PostDetailView(DetailView):
    model = Post

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
