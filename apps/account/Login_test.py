from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from django.urls import reverse

User = get_user_model()

class TestRegisterCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='amirzakov9@gmail.com',
            password='Zxcvb2009_'
        )

    def test_login_user(self):
        response = self.client.post(
            reverse('account:login'),
            data={'email': 'amirzakov9@gmail.com', 'password': 'Zxcvb2009_'},
            format='json'
        )
        self.assertEqual(response.status_code, 200)