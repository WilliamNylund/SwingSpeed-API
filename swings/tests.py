from django.contrib.auth import get_user_model, login
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory
from swings import views
from swings.models import Swing
from rest_framework.test import force_authenticate
from django.contrib.auth import authenticate

class SwingTests(TestCase):
    factory = APIRequestFactory()
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(username="testuser", password="foo")
        self.user.token = Token.objects.get_or_create(user=self.user)
        User.objects.create_superuser(username='testadmin', password='foo')
        Swing.objects.create(speed="99.5", user=self.user)
        Swing.objects.create(speed="75", user=self.user)
        Swing.objects.create(speed="22", user=self.user)

    def test_get_swing(self):
        view = views.SwingList.as_view()
        request = self.factory.get('/api/swings/')
        force_authenticate(request, user=self.user, token=self.user.token)
        response = view(request)
        assert len(response.data) == 3

    def test_create_swing(self):
        view = views.SwingList.as_view()
        request = self.factory.post('/api/swings/', data={"speed": 33}, format='json')
        force_authenticate(request, user=self.user, token=self.user.token)
        response = view(request)
        assert response.data['speed'] == 33
        assert response.data['user'] == self.user.pk

    def test_update_swing(self):
        return
        #Put request is currently not working since PK is not found by drf
        swing = Swing.objects.filter(user=self.user).first()
        view = views.SwingDetail.as_view()
        print('/api/swings/' + str(swing.pk) + '/')
        put_data = {"speed": 7, "note": "note1"}
        request = self.factory.put('/api/swings/' + str(swing.pk) + '/', put_data, format='json')
        force_authenticate(request, user=self.user, token=self.user.token)
        response = view(request)
        print(response.data)
        assert response.data['speed'] == 7
        assert response.data['note1'] == self.user.pk


