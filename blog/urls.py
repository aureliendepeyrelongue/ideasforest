from django.urls import path
from .views import (
    post_detail_view,
    post_list_view,
    user_post_list_view,
    search_results_list_view,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    ajax_like,
    contact_us_view,
    about_view)
from . import views

urlpatterns = [
    path('', post_list_view, name='blog-home'),
    path('user/posts/<int:pk>', user_post_list_view, name='user-post-list'),
    path('post/<int:pk>/', post_detail_view, name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('api/post/<int:pk>/like', ajax_like, name='like-post'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post_search/', search_results_list_view, name='search-results') , 
    path('about/', contact_us_view, name='contact-us'), 
    path('about/', about_view, name='blog-about')

]

