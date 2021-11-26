from django.contrib.auth import get_user_model, login
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory
from users import views
from rest_framework.test import force_authenticate
from django.contrib.auth import authenticate
from djoser import views as djoser_views

class UsersManagersTests(TestCase):
    def setUp(self):
        User = get_user_model()
        User.objects.create(username="testuser", password="foo")
        User.objects.create_superuser(username='testadmin', password='foo')

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
        factory = APIRequestFactory()

        """ ADMIN TESTS """
        admin_user = get_user_model().objects.get(username='testadmin')
        admin_user.token = Token.objects.get_or_create(user=admin_user)
        view = djoser_views.UserViewSet.as_view({'get': 'list'})
        request = factory.get('/auth/users/')
        force_authenticate(request, user=admin_user, token=admin_user.token)
        response = view(request)
        assert len(response.data) > 1
        assert response.status_code == 200

        """ REGULAR USER TESTS"""
        """ GET """
        user = get_user_model().objects.get(username='testuser')
        user.token = Token.objects.get_or_create(user=user)
        view = djoser_views.UserViewSet.as_view({'get': 'list'})
        request = factory.get('/auth/users/me')
        force_authenticate(request, user=user, token=user.token)
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