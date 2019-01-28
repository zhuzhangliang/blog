from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from blogs import views
from blogs.forms import CaptchaAuthenticationForm

urlpatterns = [
    # Home page.
    path('', views.index, name='index'),

    # Login page.
    path('login/', LoginView.as_view(template_name='blogs/login.html',
                                     authentication_form=CaptchaAuthenticationForm),
         name='login'),

    # Logout page.
    path('logout/', LogoutView.as_view(), name='logout'),

    # Signup page.
    path('signup/', views.signup, name='signup'),

    # Detail Page for a single post.
    path('post/<int:post_id>/', views.post, name='post'),

    # Page for adding a new post.
    path('new_post/', views.new_post, name='new_post'),

    # Page for editing an post.
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),

    # Page for deleting an post.
    path('delete_post/<int:pk>/', views.PostDeleteView.as_view(),
         name='delete_post'),

    # Page for adding new comment.
    path('post/<int:post_id>/new_comment/', views.new_comment,
         name='new_comment'),

    # Page for editing an comment.
    path('post/<int:post_id>/edit_comment/<int:comment_id>/',
         views.edit_comment, name='edit_comment'),

    # Page for deleting an comment.
    path('post/<int:post_id>/delete_comment/<int:pk>/',
         views.CommentDeleteView.as_view(), name='delete_comment'),
]
