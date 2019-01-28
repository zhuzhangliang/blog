from django.contrib.auth.models import User
from django.test import TestCase

from blogs.models import Post, Comment


class PostModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='testuser',
                                             password='1X<ISRUkw+tuK')
        Post.objects.create(subject='test_subject', content='test_content',
                            owner=test_user)

    def test_subject_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('subject').verbose_name
        self.assertEqual(field_label, 'subject')

    def test_content_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('content').verbose_name
        self.assertEqual(field_label, 'content')

    def test_create_date_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('create_date').verbose_name
        self.assertEqual(field_label, 'create date')

    def test_last_date_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('last_date').verbose_name
        self.assertEqual(field_label, 'last date')

    def test_owner_date_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('owner').verbose_name
        self.assertEqual(field_label, 'owner')

    def test_subject_max_length(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field('subject').max_length
        self.assertEqual(max_length, 200)

    def test_object_name_is_subject(self):
        post = Post.objects.get(id=1)
        expected_object_name = post.subject
        self.assertEqual(expected_object_name, str(post))


class CommentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='testuser',
                                             password='1X<ISRUkw+tuK')
        test_post = Post.objects.create(subject='test_subject',
                                        content='test_content',
                                        owner=test_user)
        Comment.objects.create(content='test_content', owner=test_user,
                               comment_post=test_post)

    def test_content_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('content').verbose_name
        self.assertEqual(field_label, 'content')

    def test_create_date_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('create_date').verbose_name
        self.assertEqual(field_label, 'create date')

    def test_last_date_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('last_date').verbose_name
        self.assertEqual(field_label, 'last date')

    def test_owner_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('owner').verbose_name
        self.assertEqual(field_label, 'owner')

    def test_comment_post_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('comment_post').verbose_name
        self.assertEqual(field_label, 'comment post')

    def test_object_name_is_content(self):
        comment = Comment.objects.get(id=1)
        expected_object_name = comment.content
        self.assertEqual(expected_object_name, str(comment))
