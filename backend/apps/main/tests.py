from django.test import TestCase
from rest_framework.test import APITestCase
from posts.models import Post


class PostListTest(APITestCase):
    def test_get_post(self):
        Post.objects.create(title='Post 1')
    
        Post.objects.create(title='Post 2')

        response = self.client.get('api/posts/')

        assert response.status_code == 200

        assert len(response.data) == 2 

