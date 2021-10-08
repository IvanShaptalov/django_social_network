from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.crypto import get_random_string
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from social_network import forms
from social_network.forms import PostForm
from social_network.models import Post, PostUser, LikeReaction
from social_network.utilities import signer
from django.core.signing import BadSignature


def index(request):
    posts = Post.objects.filter(is_active=True)
    context = {'posts': posts}
    return render(request, 'main/index.html', context)


# region registration

class RegisterUserView(CreateView):
    model = PostUser
    template_name = 'registration/register_user.html'
    form_class = forms.RegisterUserForm
    success_url = reverse_lazy('social_network:register_done')


class RegisterDoneView(TemplateView):
    template_name = 'registration/register_done.html'


def generate_api_token():
    """token to access api info
    if token already exists, try again"""
    token = get_random_string(length=32)
    if PostUser.objects.filter(api_token=token):
        generate_api_token()
    else:
        return token


def user_activate(request, sign):
    # solved test this
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'errors/bad_signature.html')
    user = get_object_or_404(PostUser, username=username)
    if user.is_activated:
        template = 'registration/user_is_activated.html'
    else:
        template = 'registration/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.api_token = generate_api_token()
        print(f'token: {user.api_token}')
        user.save()
    return render(request, template)


# endregion

# region login
class UserLoginView(LoginView):
    template_name = 'login/login.html'


class UserLogoutView(LoginRequiredMixin, LogoutView):
    template_name = login = 'login/logout.html'


# endregion

# region post operations
@login_required
def profile_post_add(request):
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
        post = form.save()
        messages.add_message(request, messages.SUCCESS,
                             'Post added')
        return redirect('social_network:profile')
    else:
        form = PostForm(initial={'author': request.user.pk})
        context = {'form': form}
        return render(request, 'main/profile_post_add.html', context)


# solved image not changed, issue - multipart/data in html
@login_required
def profile_post_change(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Post edited')
            return redirect('social_network:profile')
    else:
        form = PostForm(instance=post)
        context = {'form': form}
        return render(request, 'main/profile_post_change.html', context)


@login_required
def profile_posts(request):
    """get post from current user"""
    posts = Post.objects.all().filter(author_id=request.user.pk)
    context = {'posts': posts}
    return render(request, 'main/profile.html', context)


# endregion

# region reaction handling
@login_required
def handle_reaction(request, pk):
    """handle like, or unlike action"""
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        # if post get user and reaction from request
        user_pk = request.user.pk
        print(request)
        reaction = request.POST.get('reaction')
        # if reaction - like
        if reaction == LikeReaction.LIKE:
            liked = post.likereaction_set.filter(author_id=user_pk).first()

            # if not reaction or user unliked it
            if not liked or liked.reaction == LikeReaction.UNLIKE:
                if not liked:
                    # if unliked - write new reaction
                    reaction = LikeReaction()
                else:
                    # set that reaction is like
                    reaction = liked
                    # add post and author to reaction
                reaction.post = post
                reaction.author = request.user
                reaction.reaction = reaction.LIKE
                # commit
                reaction.save()
        # if reaction unlike analog to like
        elif reaction == LikeReaction.UNLIKE:
            unliked = post.likereaction_set.filter(author_id=user_pk).first()
            if not unliked or unliked.reaction == LikeReaction.LIKE:
                if not unliked:
                    reaction = LikeReaction()
                else:
                    reaction = unliked
                reaction.post = post
                reaction.author = request.user
                reaction.reaction = reaction.UNLIKE
                reaction.save()
        # refresh page
        return redirect('social_network:index')


# endregion

# region api_token
@login_required
def api_token(request):
    return render(request, 'main/profile_api_key.html')

# endregion
