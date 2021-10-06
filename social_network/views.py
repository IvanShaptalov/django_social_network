from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from social_network import forms
from social_network.forms import PostForm
from social_network.models import Post, PostUser


def index(request):
    posts = Post.objects.filter(is_active=True)[:10]
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


def user_posts(request):
    posts = Post.objects.all().filter(author_id=request.user.pk)
    context = {'posts': posts}
    return render(request, 'main/profile.html', context)
# endregion
