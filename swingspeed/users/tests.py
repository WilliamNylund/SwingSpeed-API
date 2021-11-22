from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory
from users import views
from rest_framework.test import force_authenticate

class UsersManagersTests(TestCase):
    def setUp(self):
        User = get_user_model()
        User.objects.create(username="testuser", password="foo")
        User.objects.create_superuser(username='testadmin', password='foo')

    def test_register(self):
        factory = APIRequestFactory()
        view = views.UserRegister.as_view()

        request = factory.post('/users/register/', {'username': 'testRegister', 'password': 'foo'})
        response = view(request)
        assert response.status_code == 201
        User = get_user_model()
        user = User.objects.get(username='testRegister')

        self.assertEqual(user.username, 'testRegister')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        token = Token.objects.get(user=user)
        self.assertTrue(token)

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
        view = views.UserList.as_view()
        request = factory.get('/users/')
        force_authenticate(request, user=admin_user, token=admin_user.token)
        response = view(request)

        assert response.status_code == 200

        """ REGULAR USER TESTS"""
        """ GET """
        user = get_user_model().objects.get(username='testuser')
        user.token = Token.objects.get_or_create(user=user)
        view = views.UserList.as_view()
        request = factory.get('/users/')
        force_authenticate(request, user=user, token=user.token)
        response = view(request)
        assert response.status_code == 403

        view = views.UserDetail.as_view()
        request = factory.get('/users/' + str(user.id))
        force_authenticate(request, user=user, token=user.token)
        response = view(request, pk=user.id)
        assert response.status_code == 200

        request = factory.get('/users/' + str(admin_user.id))
        force_authenticate(request, user=user, token=user.token)
        response = view(request, pk=admin_user.id)
        assert response.status_code == 403
        """
        PUT
        request = factory.put('/users/' + str(user.id), {'username': 'puttest'})
        force_authenticate(request, user=user, token=user.token)
        response = view(request, pk=user.id)
        print(response)
        #assert response.status_code == 403
        """
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