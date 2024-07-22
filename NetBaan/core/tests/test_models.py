from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


# helper function
def sample_user(username='randomname', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(username, password)


def sample_book(title="sample title", author="sample author", genre="sample genre"):
    """Create a sample book"""
    return models.Books.objects.create(title, author, genre)


class ModelTests(TestCase):
    def test_create_user_successful(self):
        username = "admin"
        password = "admin123"
        user = get_user_model().objects.create_user(username=username, password=password)
        self.assertEquals(user.username, username)
        self.assertTrue(user.check_password(password))

    def test_create_new_super_user(self):
        user = get_user_model().objects.create_superuser(
            username='admin',
            password='admin123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_new_book(self):
        payload = {
            "title": "new title",
            "author": "author-1",
            "genre": "genre-1"
        }
        book = models.Books.objects.create(**payload)
        self.assertEqual(str(book), book.title)







