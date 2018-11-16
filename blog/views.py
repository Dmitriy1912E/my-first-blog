from django.shortcuts import redirect
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .forms import PostForm
from django.urls import reverse


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    form = PostForm(request.POST or None)

    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()

        return redirect('post_detail', pk=post.pk)

    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None, instance=post)

    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()

        return redirect('post_detail', pk=post.pk)

    return render(request, 'blog/post_edit.html', {'form': form})


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)


    if request.method == "GET":
     
        return render(request, 'blog/post_delete.html', {"post": post})
    else:
        post.delete()
        return HttpResponseRedirect(reverse('post_list'))

