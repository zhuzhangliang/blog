from captcha.fields import CaptchaField, CaptchaTextInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from blogs.models import Post, Comment


class PostForm(forms.ModelForm):
    """Create a post form with subject and content."""
    class Meta:
        model = Post
        fields = ['subject', 'content']


class CommentForm(forms.ModelForm):
    """Create a comment form with content."""
    class Meta:
        model = Comment
        fields = ['content']


class CaptchaUserCreationForm(UserCreationForm):
    """Create a user signup form with captcha."""
    captcha = CaptchaField(
        widget=CaptchaTextInput(attrs={'placeholder': '验证码'}))


class CaptchaAuthenticationForm(AuthenticationForm):
    """Create a user login form with captcha."""
    captcha = CaptchaField(
        widget=CaptchaTextInput(attrs={'placeholder': '验证码'}))


class CaptchaAjaxForm(forms.Form):
    """Create a captcha Ajax form."""
    captcha = CaptchaField
