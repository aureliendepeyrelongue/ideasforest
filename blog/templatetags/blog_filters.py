from django import template

register = template.Library()

def get_likes_number(post):
    return post.get_likes().count()
def user_already_liked(user,post):
    return true

register.filter('get_likes_number',get_likes_number)

register.filter('user_already_liked',user_already_liked)