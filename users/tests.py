from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import CustomUser


class CustomUserRegistrationTestCase(APITestCase):

    def setUp(self):
        self.register_url = reverse('user-registration')
        self.valid_data = {
            'username': 'testuser123',
            'password': 'Test12345',
            'email': 'test@gmail.com',
            'dob': '1995-05-15',
            'credit_card_number': '1234567812345678'
        }

    def test_duplicate_username(self):
        CustomUser.objects.create_user(
            username=self.valid_data['username'], password=self.valid_data['password'], email=self.valid_data['email'])
        self._test(None, None, status.HTTP_409_CONFLICT)

    def test_valid(self):
        self._test(None, None, status.HTTP_201_CREATED)

    def test_invalid_username_whitespace(self):
        self._test('username', 'white space', status.HTTP_400_BAD_REQUEST)

    def test_invalid_username_non_alpha(self):
        self._test('username', '@|_£><', status.HTTP_400_BAD_REQUEST)

    def test_invalid_password_too_short(self):
        self._test('password', '2 short', status.HTTP_400_BAD_REQUEST)

    def test_invalid_password_no_uppercase(self):
        self._test('password', 'n0uppercase', status.HTTP_400_BAD_REQUEST)

    def test_invalid_password_no_number(self):
        self._test('password', 'NoooNumberrr', status.HTTP_400_BAD_REQUEST)

    def test_invalid_dob_wrong_format(self):
        self._test('dob', '15th of May 1995', status.HTTP_400_BAD_REQUEST)

    def test_invalid_credit_card_number_too_short(self):
        self._test('credit_card_number', '12345', status.HTTP_400_BAD_REQUEST)

    def test_invalid_credit_card_number_too_long(self):
        self._test('credit_card_number', '123456789123456789',
                   status.HTTP_400_BAD_REQUEST)

    def test_invalid_dob_too_young(self):
        young_dob = (timezone.now().date() -
                     timezone.timedelta(days=365*16)).isoformat()
        self._test('dob', young_dob, status.HTTP_403_FORBIDDEN)

    def _test(self, field: str = None, value: str = None, status_code: status = status.HTTP_200_OK):
        if not None in [field, value]:
            self.valid_data[field] = value
        response = self.client.post(self.register_url, self.valid_data)
        try:
            self.assertEqual(response.status_code, status_code)
        except AssertionError as ae:
            raise ae


class GetUsersTestCase(APITestCase):

    def setUp(self):
        self.get_users_url = reverse('user-registration')

        CustomUser.objects.create_user(
            username='user_with_cc', password='Test12345', email='email1@gmail.com', credit_card_number='1234567812345678')
        CustomUser.objects.create_user(
            username='user_without_cc', password='Test12345', email='email2@gmail.com',)

    def test_get_users_with_credit_card(self):
        response = self.client.get(self.get_users_url, {'CreditCard': 'Yes'})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'user_with_cc')

    def test_get_users_without_credit_card(self):
        response = self.client.get(self.get_users_url, {'CreditCard': 'No'})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'user_without_cc')

    def test_get_all_users(self):
        response = self.client.get(self.get_users_url)
        self.assertEqual(len(response.data), 2)
