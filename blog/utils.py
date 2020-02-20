from .models import Post, Like

def get_posts_and_likes(request):
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

    return list_
