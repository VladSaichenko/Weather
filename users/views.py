from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import authenticate, login
from weather.models import Post


def response_custom403page(request, exception=None):
    return render(request, 'page403.html', status=403)


def response_custom404page(request, exception=None):
    return render(request, 'page404.html', status=404)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)

            return redirect('/')
    else:
        form = UserRegisterForm()

    return render(request, 'register_page.html', {'form': form})


@login_required(login_url='login')
def profile(request):
    posts = Post.objects.all().filter(author=request.user).order_by('-date_posted')

    return render(request, 'profilepage.html', {'posts': posts})


@login_required(login_url='login')
def editprofile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profilepage_settings.html', context)
