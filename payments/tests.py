from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import CustomUser


class PaymentTests(APITestCase):

    def setUp(self):

        self.payments_url = reverse('payments')

        CustomUser.objects.create_user(
            username='testuser123',
            password='Test12345',
            email='test@gmail.com',
            dob='1995-05-15',
            credit_card_number='1234567812345678'
        )

        self.valid_data = {
            "credit_card_number": 1234567812345678,
            "amount": 123
        }

    def test_valid_payment(self):
        self._test(None, None, status.HTTP_201_CREATED)

    def test_invalid_credit_card_length(self):
        self._test('credit_card_number', '1234567812345',
                   status.HTTP_400_BAD_REQUEST)

    def test_unregistered_credit_card(self):
        self._test('credit_card_number', '9876543212345678',
                   status.HTTP_404_NOT_FOUND)

    def test_invalid_amount_non_numeric(self):
        self._test('amount', '10A', status.HTTP_400_BAD_REQUEST)

    def test_invalid_amount_too_long(self):
        self._test('amount', '9000', status.HTTP_400_BAD_REQUEST)

    def _test(self, field: str = None, value: str = None, status_code: status = status.HTTP_200_OK):
        if not None in [field, value]:
            self.valid_data[field] = value
        response = self.client.post(self.payments_url, self.valid_data)
        try:
            self.assertEqual(response.status_code, status_code)
        except AssertionError as ae:
            raise ae
