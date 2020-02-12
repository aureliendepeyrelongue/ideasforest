from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.models import User
from blog.models import Post

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Votre compte a été créé {username} ! Vous pouvez à présent vous connecter.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def user_detail(request,username):
    user = get_object_or_404(User, username=username)
    posts_counting = Post.objects.filter(author=user).count()
    return render(request, 'users/user_detail.html',{'user': user, 'posts_counting': posts_counting})

@login_required
def profile(request):

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
             u_form.save()
             p_form.save()
             messages.success(request,f'Votre compte est mis à jour.')
             return redirect('profile')
    else :
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form':u_form,
        'p_form':p_form,
        'update_profil_active': 'active'
    }
    return render(request, 'users/profile.html',context)


    
