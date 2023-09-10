from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from rest_framework import serializers, status

from users.models import CustomUser


class CustomUserSerializer(serializers.Serializer):
    username = serializers.CharField(validators=[RegexValidator(
        r'^[a-zA-Z0-9]+$', 'Username should be alphanumeric and contain no spaces.')])
    password = serializers.CharField(validators=[RegexValidator(
        r'^(?=.*[A-Z])(?=.*\d).{8,}$', 'Password should have a minimum length of 8, at least one uppercase letter and one number.')])
    email = serializers.EmailField()
    dob = serializers.DateField(input_formats=['%Y-%m-%d'])
    credit_card_number = serializers.CharField(validators=[RegexValidator(
        r'^\d{16}$', 'Credit card number should have 16 digits.')], required=False)

    def validate(self, data):
        self._check_age(data['dob'])
        self._check_user_already_exists(data['username'])
        return data

    def _check_age(self, dob):
        today = datetime.now().date()
        age = today.year - dob.year - \
            ((today.month, today.day) < (dob.month, dob.day))
        if age < 18:
            self.http_error = status.HTTP_403_FORBIDDEN
            raise serializers.ValidationError("User is under the age of 18.")

    def _check_user_already_exists(self, username):
        if CustomUser.objects.filter(username=username).exists():
            self.http_error = status.HTTP_409_CONFLICT
            raise serializers.ValidationError(
                "Username has already been used.")
