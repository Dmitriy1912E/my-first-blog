from django.http import HttpResponseForbidden
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .forms import PostForm
from django.urls import reverse
from .forms import AuthForm
from django.contrib.auth import login as django_login, logout as django_logout
from .forms import CommentForm
from .models import Comment
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from .forms import ProfileForm

def home(request):
    return render(request, 'blog/base.html')


def comment_permissions(view):
    def _wrap(request, post_pk, comment_pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=comment_pk)
        if comment.author != request.user and not request.user.is_superuser:
            return HttpResponseForbidden()

        return view(request, comment, post_pk, *args, **kwargs)

    return _wrap


def post_permissions(view):
    def _wrap(request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        if post.author != request.user or not request.user.is_superuser:
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
    form = PostForm(request.POST or None, files=request.FILES or None)

    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('post_detail', pk=post.pk)

    return render(request, 'blog/post_edit.html', {'form': form})


@post_permissions
def post_edit(request, post):
    form = PostForm(data=request.POST or None, files=request.FILES or None, instance=post)

    if form.is_valid():
        post = form.save(commit=False)
        post.status = 'moderation'
        post.save()

        return HttpResponseRedirect(request.GET.get('next', '/'))
    return render(request, 'blog/post_edit.html', context={'form': form})


@post_permissions
def post_delete(request, post):
    if request.method == "GET":
        return render(request, 'blog/post_delete.html', {"post": post})
    else:
        post.delete()
        return HttpResponseRedirect(reverse('post_list'))


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')  # well done, but you forgot empty line
    form = AuthForm(request.POST or None)
    if form.is_valid():
        if request.user is not None:
            django_login(request, form.cleaned_data['user'])
            return HttpResponseRedirect(request.GET.get('next', '/'))

    return render(request, 'blog/user_login.html', context={'form': form})


def logout(request):
    django_logout(request)
    return HttpResponseRedirect(request.GET.get('next', '/'))


def comment_new(request, post_pk):
    form = CommentForm(request.POST or None)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post_id = post_pk
        comment.save()
        return redirect('post_detail', pk=post_pk)

    return render(request, 'blog/post_detail.html', context={'post_pk': post_pk})


@comment_permissions
def comment_delete(request, comment, post_pk):
    comment.delete()
    return HttpResponseRedirect(reverse('post_detail', args=(post_pk,)))


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('user_login')
    template_name = 'blog/signup.html'


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('blog/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your blog account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')

    else:
        form = SignupForm()

    return render(request, 'blog/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        django_login(request, user)
        # return redirect('home')
        return render(request, 'blog/succeful_activasion.html')
    else:
        return HttpResponse('Activation link is invalid!')


def profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'blog/profile.html', {'profile_user': user})


def profile_edit(request, username, profile):
    user = get_object_or_404(User, username=username)
    if user != profile.user and not request.user_is_superuser:
        return HttpResponseForbidden
    form = ProfileForm(data=request.GET or None, files=request.FILES or None, instance=profile)

    if form.is_valid():
        profile = form.save(commit=False)
        profile.save()

        return HttpResponseRedirect(request.GET.get('next', '/'))
    return render(request, 'blog/profile_edit.html', context={'form': form})
