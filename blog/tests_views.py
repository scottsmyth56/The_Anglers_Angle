from django.test import TestCase
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Post,User

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
    

class PostViewTests(SetUpClass):
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
        
        self.edit_post_url = reverse('editPost', kwargs={'pk': self.post.pk}) 
        
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
