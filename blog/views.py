from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .forms import PostForm
from django.urls import reverse
from .forms import AuthForm
from django.contrib.auth import authenticate, login as django_login


def post_permissions(view):
    def _wrap(request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        if post.author != request.user and not request.user.is_superuser:
            return HttpResponseForbidden()

        return view(request, post, *args, **kwargs)

    return _wrap


def post_list(request):
    posts = Post.objects.filter(status='active', published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, status='active')
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    form = PostForm(request.POST or None)

    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('post_detail', pk=post.pk)

    return render(request, 'blog/post_edit.html', {'form': form})


@post_permissions
def post_edit(request, post):
    form = PostForm(request.POST or None, instance=post)

    if form.is_valid():
        post = form.save(commit=False)
        post.status = 'moderation'
        post.save()

        return redirect('post_detail', pk=post.pk)

    return render(request, 'blog/post_edit.html', context={'form': form})


@post_permissions
def post_delete(request, post):
    if request.method == "GET":
        return render(request, 'blog/post_delete.html', {"post": post})
    else:
        post.delete()
        return HttpResponseRedirect(reverse('post_list'))


def login(request):
    form = AuthForm(request.POST or None)
    if form.is_valid():
        if request.user is not None:
            django_login(request, form.cleaned_data['user'])

            return HttpResponseRedirect(request.GET.get('next', '/'))

    return render(request, 'blog/user_login.html', context={'form': form})
