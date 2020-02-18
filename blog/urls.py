from django.urls import path
from .views import (
    PostListView, 
    post_detail_view,
    post_list_view,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    SearchPostListView)
from . import views

urlpatterns = [
    path('', post_list_view, name='blog-home'),
     path('user-test/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', post_detail_view, name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post_search/', SearchPostListView.as_view(), name='search_results') ,  
    path('about/', views.about, name='blog-about')

]

