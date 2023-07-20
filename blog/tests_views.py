from django.test import TestCase
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Post,User,Like,Comment
from django.shortcuts import get_object_or_404

class SetUpClass(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        
        
class IndexViewTests(SetUpClass):
    def setUp(self):
        super().setUp()
        self.index_url = reverse('index') 
        
        Post.objects.create(user_id=self.user, title="Test Title 1", content="Test Post 1")
        Post.objects.create(user_id=self.user, title="Test Title 2", content="Test Post 2")
    
    def test_not_logged_in_redirects_to_login(self):
        response = self.client.get(self.index_url)
        login_url = reverse('login')
        self.assertRedirects(response, f'{login_url}?next={self.index_url}')

    def test_logged_in_redirects_to_index(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.index_url)

        self.assertEqual(str(response.context['user']), 'testuser')
        self.assertTemplateUsed(response, 'index.html')

    def test_context_data_values(self):
        login = self.client.login(username='testuser', password='12345')
        response = self.client.get(self.index_url)
    
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'], self.user)
        self.assertQuerysetEqual(
            response.context['posts'], 
            ['<Post: Test Title 1>', '<Post: Test Title 2>'], 
            ordered=False
    )
        
        
class AddPostViewTests(SetUpClass):
    def setUp(self):
        super().setUp()
        self.add_post_url = reverse('addPost')
        
    def test_correct_template_loads(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.add_post_url)

        
        self.assertEqual(str(response.context['user']), 'testuser')
        self.assertTemplateUsed(response, 'Posts/add_post.html')

    def test_successfully_create_post(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(self.add_post_url, {
            'title': 'Test Title',
            'content': 'Test Content',
            'image1': 'placeholder',
            'image2': 'placeholder',
            'category': 'Test Category',  
        })

     
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().title, 'Test Title')

    def test_success_message_after_creating_post(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(self.add_post_url, {
            'title': 'Test Title',
            'content': 'Test Content',
            'image1': 'placeholder',
            'image2': 'placeholder',
            'category': 'Test Category',
        },follow=True)


        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), 'Post added Succesfully')
    

class PostTests(SetUpClass):
    def setUp(self):
        super().setUp()
        
        self.post = Post.objects.create(
            user_id=self.user, 
            title="Test Title 1", 
            content="Test Post 1", 
            image1='placeholder', 
            image2='placeholder', 
            category="Test Category"
        )
        
        Like.objects.create(user_id=self.user, post_id=self.post)
        
        self.edit_post_url = reverse('editPost', kwargs={'pk': self.post.pk}) 
        self.delete_post_url = reverse('deletePost', kwargs={'pk': self.post.pk})
        self.view_post_url = reverse('viewPost', kwargs={'pk': self.post.pk})
        self.like_post_url = reverse('likePost', kwargs={'pk': self.post.pk})
        self.unlike_post_url = reverse('unlikePost', kwargs={'pk': self.post.pk})


    def test_successfully_update_post(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(self.edit_post_url, {
            'title': 'Updated Test Title',
            'content': 'Updated Test Content',
            'image1': 'placeholder',
            'image2': 'placeholder',
            'category': 'Updated Test Category',
        })

        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Test Title')
        self.assertEqual(self.post.content, 'Updated Test Content')
        self.assertEqual(self.post.category, 'Updated Test Category')

    def test_successfully_delete_post(self):
        self.client.login(username='testuser', password='12345')
        initial_post_count = Post.objects.count()
        response = self.client.post(self.delete_post_url, follow=True)

        self.assertEqual(Post.objects.count(), initial_post_count-1)
    
    def test_view_post_successfully(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.view_post_url)

        self.assertEqual(str(response.context['user']), 'testuser')
        self.assertTemplateUsed(response, 'Posts/post_detail.html')
        self.assertEqual(response.context['post'], self.post)
        
    def test_like_post_successfully(self):
        self.client.login(username='testuser', password='12345')
        Like.objects.filter(post_id=self.post.pk, user_id=self.user.pk).delete()
        initial_like_count = Like.objects.count()
        response = self.client.post(self.like_post_url)

        self.assertEqual(Like.objects.count(), initial_like_count+1)
        like = get_object_or_404(Like, post_id=self.post.pk, user_id=self.user.pk)
        self.assertIsNotNone(like)
        
    def test_unlike_post_successfully(self):
        self.client.login(username='testuser', password='12345')
        initial_like_count = Like.objects.count()
        response = self.client.post(self.unlike_post_url)

        self.assertEqual(Like.objects.count(), initial_like_count-1)
        like = Like.objects.filter(post_id=self.post.pk, user_id=self.user.pk).first()
        self.assertIsNone(like)
        
class CommentTests(SetUpClass):
    def setUp(self):
        super().setUp()
        self.post = Post.objects.create(
            user_id=self.user, 
            title="Test Title 1", 
            content="Test Post 1", 
            image1='placeholder', 
            image2='placeholder', 
            category="Test Category"
        )
        
        self.add_comment_url = reverse('addComment', kwargs={'pk': self.post.pk})
        

    def test_add_comment_successfully(self):
        self.client.login(username='testuser', password='12345')
        initial_comment_count = Comment.objects.count()
        response = self.client.post(self.add_comment_url, {
            'comment': 'Test Comment',
        })

        self.assertEqual(Comment.objects.count(), initial_comment_count + 1)
        comment = get_object_or_404(Comment, post_id=self.post.pk, user_id=self.user.pk)
        self.assertIsNotNone(comment)

    def test_edit_comment_successfully(self):
            self.comment = Comment.objects.create(
            user_id=self.user, 
            post_id=self.post, 
            comment="Original Comment"
            )
            
            self.edit_comment_url = reverse('editComment', kwargs={'pk': self.comment.pk})
            self.client.login(username='testuser', password='12345')
            response = self.client.post(self.edit_comment_url, {
                'comment': 'Updated Comment',
            })

            self.comment.refresh_from_db()
            self.assertEqual(self.comment.comment, 'Updated Comment')
            
    def test_delete_comment_successfully(self):
        self.client.login(username='testuser', password='12345')
        self.comment = Comment.objects.create(
            user_id=self.user, 
            post_id=self.post, 
            comment="Test Comment"
        )
        self.delete_comment_url = reverse('deleteComment', kwargs={'pk': self.comment.pk})
        initial_comment_count = Comment.objects.count()
        response = self.client.post(self.delete_comment_url)

        self.assertEqual(Comment.objects.count(), initial_comment_count - 1)
        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(pk=self.comment.pk)