from django.contrib.auth import get_user_model, login
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory
from users import views
from rest_framework.test import force_authenticate
from django.contrib.auth import authenticate
from djoser import views as djoser_views

class UsersManagersTests(TestCase):
    factory = APIRequestFactory()
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(username="testuser", password="foo")
        self.user.token = Token.objects.get_or_create(user=self.user)
        self.admin_user = User.objects.create_superuser(username='testadmin', password='foo')
        self.admin_user.token = Token.objects.get_or_create(user=self.admin_user)

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(username='normaluser', password='foo', email='normal@user.com')
        self.assertEqual(user.username, 'normaluser')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(username='')
        with self.assertRaises(ValueError):
            User.objects.create_user(username='', password="foo")


    def test_get_user(self):
        """ ADMIN TESTS """
        view = djoser_views.UserViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/users/')
        force_authenticate(request, user=self.admin_user, token=self.admin_user.token)
        response = view(request)
        assert len(response.data) > 1
        assert response.status_code == 200

        """ REGULAR USER TESTS"""
        """ GET """
        view = djoser_views.UserViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/users/me')
        force_authenticate(request, user=self.user, token=self.user.token)
        response = view(request)
        assert len(response.data) == 1
        assert response.status_code == 200

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(username='superusername', password='foo')
        self.assertEqual(admin_user.username, 'superusername')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                username='superusername', password='foo', is_superuser=False)