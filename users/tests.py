from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.serializers import UserSerializer


class MyAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="user@aa.com")
        self.item1 = User.objects.create(email="a@aa.com")
        self.item2 = User.objects.create(email="b@aa.com")
        self.list_url = reverse('users-list')  # Assuming you have a router setup
        self.detail_url = reverse('users-detail', args=[self.item1.pk])
        access_token = self.get_jwt_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def get_jwt_token(self):
        # Manually create tokens for the user
        refresh = RefreshToken.for_user(self.user)
        return str(refresh.access_token)

    def test_list_Users(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = UserSerializer([self.user,self.item1, self.item2], many=True)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_User(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = UserSerializer(self.item1)
        self.assertEqual(response.data, serializer.data)

    def test_create_User(self):
        data = {'email': 'xx@xx.com', 'password': '123', 'password2':'123'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 4)
        self.assertEqual(User.objects.get(email='xx@xx.com').email, 'xx@xx.com')

