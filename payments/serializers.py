from django.core.validators import RegexValidator
from rest_framework import serializers, status

from users.models import CustomUser


class PaymentSerializer(serializers.Serializer):
    credit_card_number = serializers.CharField(validators=[RegexValidator(
        r'^\d{16}$', 'Credit card number should have 16 digits.')])
    amount = serializers.CharField(validators=[RegexValidator(
        r'^\d{1,3}$', 'Credit card number should have 3 digits.')])

    def validate(self, data):
        self._check_credit_card_number_exists(data['credit_card_number'])
        return data

    def _check_credit_card_number_exists(self, credit_card_number):
        if not CustomUser.objects.filter(credit_card_number=credit_card_number).exists():
            self.http_error = status.HTTP_404_NOT_FOUND
            raise serializers.ValidationError(
                "Credit card number not registered.")
