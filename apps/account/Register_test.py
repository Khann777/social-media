from django.test import TestCase
from rest_framework.test import APIRequestFactory


class TestRegisterCase(TestCase):
    def test_register_user(self):
        factory = APIRequestFactory()


        data = {
            'email': 'amirzakov9@gmail.com',
            'password': 'zxcvb2009',
            'password_confirm': 'zxcvb2009',
            'first_name': 'Amir',
            'last_name': 'Zakov'
        }


        request = factory.post('/register/', data, format='json')


        from apps.account.views import RegisterView
        view = RegisterView.as_view()
        response = view(request)


        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['email'], 'amirzakov9@gmail.com')