from rest_framework.test import APIClient
from rest_framework import status
import pytest

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user(db):
    from django.contrib.auth.models import User
    return User.objects.create_user(
        username="testuser", 
        password="password123"
    )

def test_create_post(client, user, db):
    client.force_authenticate(user=user)
    response = client.post("/api/posts/", {
        "title": "Тест",
        "content": "Контент"
    })
    assert response.status_code == status.HTTP_201_CREATED

def test_create_post_unauthorized(client, db):
    response = client.post("/api/posts/", {
        "title": "Тест",
        "content": "Контент"
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_posts(client, db):
    response = client.get("/api/posts/")
    assert response.status_code == status.HTTP_200_OK