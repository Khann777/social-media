# from rest_framework.test import APITestCase
# from django.urls import reverse
# from knox.models import AuthToken
# from rest_framework import status
# from apps.account.models import CustomUser
#
#
# class LogoutTestCase(APITestCase):
#     def setUp(self):
#         self.user = CustomUser.objects.create_user(
#             email='testuser@example.com',
#             password='password123'
#         )
#
#
#         self.token = AuthToken.objects.create(user=self.user)[1]
#
#     def test_logout(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
#
#
#         response = self.client.post(reverse('account:logout'))
#
#
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#
#
#         token_exists = AuthToken.objects.filter(user=self.user).exists()
#         self.assertFalse(token_exists)