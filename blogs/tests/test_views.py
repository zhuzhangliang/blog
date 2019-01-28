from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blogs.models import Post, Comment


class IndexViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs/index.html')


class SignupViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs/signup.html')

    def test_redirect_if_user_register_success(self):
        response = self.client.post(reverse('signup'),
                                    data={'username': 'testuser',
                                          'password1': '1X<ISRUkw+tuK',
                                          'password2': '1X<ISRUkw+tuK',
                                          'captcha_0': 'testcaptcha',
                                          'captcha_1': 'PASSED'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')


class PostViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='testuser',
                                             password='1X<ISRUkw+tuK')
        test_post = Post.objects.create(subject='test_subject',
                                        content='test_content',
                                        owner=test_user)
        Comment.objects.create(content='test_content', owner=test_user,
                               comment_post=test_post)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/post/1/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('post', kwargs={'post_id': 1}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('post', kwargs={'post_id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs/post.html')


class NewPostViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='testuser',
                                             password='1X<ISRUkw+tuK')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/new_post/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login?next=/new_post/'))

    def test_redirect_if_not_logged_in_by_name(self):
        response = self.client.get(reverse('new_post'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login?next=/new_post/'))

    def test_redirect_if_logged_in(self):
        self.client.login(username='testuser', password='1X<ISRUkw+tuK')
        response = self.client.get('/new_post/')
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_logged_in_by_name(self):
        self.client.login(username='testuser', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('new_post'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('new_post'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs/new_post.html')

    def test_redirects_to_new_post_publish_on_success(self):
        self.client.login(username='testuser', password='1X<ISRUkw+tuK')
        response = self.client.post(reverse('new_post'),
                                    {'subject': 'test_new_subject',
                                     'content': 'test_new_content'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/post/1/')


class EditPostViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1',
                                              password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2',
                                              password='2HJ1vRV0Z&3iD')

        test_post1 = Post.objects.create(subject='test_subject',
                                         content='test_content',
                                         owner=test_user1)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/edit_post/1/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login?next=/edit_post/1/'))

    def test_redirect_if_not_logged_in_by_name(self):
        response = self.client.get(reverse('edit_post', kwargs={'post_id': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login?next=/edit_post/1/'))

    def test_redirect_if_logged_in(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/edit_post/1/')
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_logged_in_by_name(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('edit_post', kwargs={'post_id': 1}))
        self.assertEqual(response.status_code, 200)

    def test_edit_not_exist_post(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('edit_post', kwargs={'post_id': 2}))
        self.assertEqual(response.status_code, 404)

    def test_other_user_edit_post(self):
        self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('edit_post', kwargs={'post_id': 1}))
        self.assertEqual(response.status_code, 403)

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('edit_post', kwargs={'post_id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs/edit_post.html')

    def test_redirects_to_edit_post_on_success(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.post(
            reverse('edit_post', kwargs={'post_id': 1}),
            {'subject': 'test_edit_subject',
             'content': 'test_edit_content'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/post/1/')


class DeletePostViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1',
                                              password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2',
                                              password='2HJ1vRV0Z&3iD')

        test_post1 = Post.objects.create(subject='test_subject',
                                         content='test_content',
                                         owner=test_user1)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/delete_post/1/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login?next=/delete_post/1/'))

    def test_redirect_if_not_logged_in_by_name(self):
        response = self.client.get(reverse('delete_post', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login?next=/delete_post/1/'))

    def test_redirect_if_logged_in(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/delete_post/1/')
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_logged_in_by_name(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('delete_post', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_delete_not_exist_post(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('delete_post', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 404)

    def test_other_user_delete_post(self):
        self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('delete_post', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 403)

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('delete_post', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs/post_confirm_delete.html')

    def test_redirects_to_delete_post_on_success(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.post(reverse('delete_post', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')


class NewCommentViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='testuser',
                                             password='1X<ISRUkw+tuK')
        test_post = Post.objects.create(subject='test_subject',
                                        content='test_content',
                                        owner=test_user)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/post/1/new_comment/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            response.url.startswith('/login?next=/post/1/new_comment/'))

    def test_redirect_if_not_logged_in_by_name(self):
        response = self.client.get(
            reverse('new_comment', kwargs={'post_id': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            response.url.startswith('/login?next=/post/1/new_comment/'))

    def test_redirect_if_logged_in(self):
        self.client.login(username='testuser', password='1X<ISRUkw+tuK')
        response = self.client.get('/post/1/new_comment/')
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_logged_in_by_name(self):
        self.client.login(username='testuser', password='1X<ISRUkw+tuK')
        response = self.client.get(
            reverse('new_comment', kwargs={'post_id': 1}))
        self.assertEqual(response.status_code, 200)

    def test_comment_not_exist_post(self):
        self.client.login(username='testuser', password='1X<ISRUkw+tuK')
        response = self.client.get(
            reverse('new_comment', kwargs={'post_id': 2}))
        self.assertEqual(response.status_code, 404)

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser', password='1X<ISRUkw+tuK')
        response = self.client.get(
            reverse('new_comment', kwargs={'post_id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs/new_comment.html')

    def test_redirects_to_comment_post_on_success(self):
        self.client.login(username='testuser', password='1X<ISRUkw+tuK')
        response = self.client.post(
            reverse('new_comment', kwargs={'post_id': 1}),
            {'content': 'test_new_content'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/post/1/')


class EditCommentViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1',
                                              password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2',
                                              password='2HJ1vRV0Z&3iD')

        test_post1 = Post.objects.create(subject='test_subject1',
                                         content='test_content1',
                                         owner=test_user1)

        test_post2 = Post.objects.create(subject='test_subject2',
                                         content='test_content2',
                                         owner=test_user2)

        test_comment1 = Comment.objects.create(content='test_content1',
                                               owner=test_user1,
                                               comment_post=test_post1)

        test_comment2 = Comment.objects.create(content='test_content1',
                                               owner=test_user1,
                                               comment_post=test_post2)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/post/1/edit_comment/1/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            response.url.startswith('/login?next=/post/1/edit_comment/1/'))

    def test_redirect_if_not_logged_in_by_name(self):
        response = self.client.get(
            reverse('edit_comment', kwargs={'post_id': 1, 'comment_id': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            response.url.startswith('/login?next=/post/1/edit_comment/1/'))

    def test_redirect_if_logged_in(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/post/1/edit_comment/1/')
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_logged_in_by_name(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(
            reverse('edit_comment', kwargs={'post_id': 1, 'comment_id': 1}))
        self.assertEqual(response.status_code, 200)

    def test_edit_not_exist_post_or_comment(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(
            reverse('edit_comment', kwargs={'post_id': 3, 'comment_id': 1}))
        self.assertEqual(response.status_code, 404)
        response = self.client.get(
            reverse('edit_comment', kwargs={'post_id': 1, 'comment_id': 3}))
        self.assertEqual(response.status_code, 404)

    def test_other_user_edit_comment(self):
        self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(
            reverse('edit_comment', kwargs={'post_id': 1, 'comment_id': 1}))
        self.assertEqual(response.status_code, 403)

    def test_edit_not_current_post_comment(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(
            reverse('edit_comment', kwargs={'post_id': 2, 'comment_id': 1}))
        self.assertEqual(response.status_code, 404)

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(
            reverse('edit_comment', kwargs={'post_id': 1, 'comment_id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs/edit_comment.html')

    def test_redirects_to_edit_comment_on_success(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.post(
            reverse('edit_comment', kwargs={'post_id': 1, 'comment_id': 1}),
            {'content': 'test_edit_content'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/post/1/')


class DeleteCommentViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1',
                                              password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2',
                                              password='2HJ1vRV0Z&3iD')

        test_post1 = Post.objects.create(subject='test_subject1',
                                         content='test_content1',
                                         owner=test_user1)

        test_post2 = Post.objects.create(subject='test_subject2',
                                         content='test_content2',
                                         owner=test_user1)

        test_comment1 = Comment.objects.create(content='test_content1',
                                               owner=test_user1,
                                               comment_post=test_post1)

        test_comment2 = Comment.objects.create(content='test_content1',
                                               owner=test_user1,
                                               comment_post=test_post2)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/post/1/delete_comment/1/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            response.url.startswith('/login?next=/post/1/delete_comment/1/'))

    def test_redirect_if_not_logged_in_by_name(self):
        response = self.client.get(
            reverse('delete_comment', kwargs={'post_id': 1, 'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            response.url.startswith('/login?next=/post/1/delete_comment/1/'))

    def test_redirect_if_logged_in(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/post/1/delete_comment/1/')
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_logged_in_by_name(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(
            reverse('delete_comment', kwargs={'post_id': 1, 'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_delete_not_exist_comment_or_post(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(
            reverse('delete_comment', kwargs={'post_id': 1, 'pk': 2}))
        self.assertEqual(response.status_code, 404)
        response = self.client.get(
            reverse('delete_comment', kwargs={'post_id': 2, 'pk': 1}))
        self.assertEqual(response.status_code, 404)

    def test_other_user_delete_post(self):
        self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(
            reverse('delete_comment', kwargs={'post_id': 1, 'pk': 1}))
        self.assertEqual(response.status_code, 403)

    def test_delete_not_current_post_comment(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(
            reverse('delete_comment', kwargs={'post_id': 1, 'pk': 2}))
        self.assertEqual(response.status_code, 404)

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(
            reverse('delete_comment', kwargs={'post_id': 1, 'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs/comment_confirm_delete.html')

    def test_redirects_to_delete_comment_on_success(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.post(
            reverse('delete_comment', kwargs={'post_id': 1, 'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/post/1/')
