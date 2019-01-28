import json

from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore

from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404, \
    HttpResponse
from django.shortcuts import render, get_object_or_404

from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, CreateView

from blogs.forms import PostForm, CommentForm, CaptchaUserCreationForm, \
    CaptchaAjaxForm
from blogs.models import Post, Comment


def index(request):
    """The home page for Blog, Show all posts."""
    posts = Post.objects.all().order_by('-create_date', '-id')
    context = {'posts': posts}
    return render(request, 'blogs/index.html', context)


def signup(request):
    """Register a new user."""
    if request.method != 'POST':
        # Display blank registration form.
        form = CaptchaUserCreationForm()
    else:
        # Process completed form.
        form = CaptchaUserCreationForm(data=request.POST)

        if form.is_valid():
            form.save()
            # Register success, and then redirect to signup page.
            return HttpResponseRedirect(reverse('login'))

    context = {'form': form}
    return render(request, 'blogs/signup.html', context)


def post(request, post_id):
    """Show a single post, and all its comments."""
    post = get_object_or_404(Post, id=post_id)
    post_comments = post.comment_set.all().order_by('-create_date', '-id')

    context = {'post': post, 'post_comments': post_comments}
    return render(request, 'blogs/post.html', context)


@login_required
def new_post(request):
    """Add a new post."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = PostForm()
    else:
        # POST data submitted; process data.
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.owner = request.user
            new_post.save()
            return HttpResponseRedirect(reverse('post', args=[new_post.id]))

    context = {'form': form}
    return render(request, 'blogs/new_post.html', context)


@login_required
def edit_post(request, post_id):
    """Edit an existing post."""
    post = get_object_or_404(Post, id=post_id)

    # Make sure the post belongs to the current user.
    if post.owner != request.user:
        return HttpResponseForbidden('<h1>403 Forbidden</h1>')

    if request.method != 'POST':
        # Initial request; pre-fill form with the current post.
        form = PostForm(instance=post)
    else:
        # POST data submitted; process data.
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('post', args=[post.id]))

    context = {'post': post, 'form': form}
    return render(request, 'blogs/edit_post.html', context)


class PostDeleteView(UserPassesTestMixin, DeleteView):
    """Delete an existing post."""
    model = Post
    success_url = reverse_lazy('index')

    def test_func(self):
        # Make sure the post belongs to the current user.
        self.object = self.get_object()
        return self.object.owner == self.request.user


@login_required
def new_comment(request, post_id):
    """Add a new comment."""
    post = get_object_or_404(Post, id=post_id)
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = CommentForm()
    else:
        # POST data submitted; process data.
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.owner = request.user
            new_comment.comment_post = post
            new_comment.save()
            return HttpResponseRedirect(reverse('post', args=[post.id]))

    context = {'form': form}
    return render(request, 'blogs/new_comment.html', context)


@login_required
def edit_comment(request, post_id, comment_id):
    """Edit an existing comment."""
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, id=comment_id)

    # Make sure the post belongs to the current user.
    if comment.owner != request.user:
        return HttpResponseForbidden('<h1>403 Forbidden</h1>')

    # Make sure the comment belongs to the current post.
    if post.id != comment.comment_post.id:
        raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current comment.
        form = CommentForm(instance=comment)
    else:
        # POST data submitted; process data.
        form = CommentForm(instance=comment, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('post', args=[post.id]))

    context = {'comment': comment, 'form': form}
    return render(request, 'blogs/edit_comment.html', context)


class CommentDeleteView(UserPassesTestMixin, DeleteView):
    """Delete an existing comment."""
    model = Comment

    def get(self, request, *args, **kwargs):
        """Make sure the comment belongs to the current post."""
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        comment = get_object_or_404(Comment, id=self.kwargs.get('pk'))

        if post.id == comment.comment_post_id:
            return super().get(request, *args, **kwargs)
        else:
            raise Http404

    def post(self, request, *args, **kwargs):
        """Make sure the comment belongs to the current post"""
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        comment = get_object_or_404(Comment, id=self.kwargs.get('pk'))

        if post.id == comment.comment_post_id:
            return super().post(request, *args, **kwargs)
        else:
            raise Http404

    def get_success_url(self):
        # Delete success and then redirect to current post page.
        post_id = self.kwargs.get('post_id')
        return reverse('post', args=[post_id])

    def test_func(self):
        # Make sure the post belongs to the current user.
        self.object = self.get_object()
        return self.object.owner == self.request.user


class CaptchaAjax(CreateView):
    """Add a ajax captcha"""
    template_name = ''
    form_class = CaptchaAjaxForm

    def form_invalid(self, form):
        if self.request.is_ajax():
            to_json_response = dict()
            to_json_response['status'] = 0
            to_json_response['form_errors'] = form.errors

            to_json_response['new_cptch_key'] = CaptchaStore.generate_key()
            to_json_response['new_cptch_image'] = captcha_image_url(
                to_json_response['new_cptch_key'])

            return HttpResponse(json.dumps(to_json_response),
                                content_type='application/json')

    def form_valid(self, form):
        form.save()
        if self.request.is_ajax():
            to_json_response = dict()
            to_json_response['status'] = 1

            to_json_response['new_cptch_key'] = CaptchaStore.generate_key()
            to_json_response['new_cptch_image'] = captcha_image_url(
                to_json_response['new_cptch_key'])

            return HttpResponse(json.dumps(to_json_response),
                                content_type='application/json')
