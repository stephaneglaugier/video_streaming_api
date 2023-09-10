from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser
from .serializers import CustomUserSerializer


class UserRegistration(APIView):

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            user_data = serializer.validated_data
            try:
                CustomUser.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password'],
                    dob=user_data['dob'],
                    credit_card_number=user_data.get(
                        'credit_card_number', None)
                )
                return Response({"detail": "User created successfully."}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if hasattr(serializer, "http_error"):
            return Response(serializer.errors, status=serializer.http_error)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        credit_card_filter = request.query_params.get('CreditCard', None)

        if credit_card_filter == "Yes":
            users = CustomUser.objects.exclude(
                credit_card_number__isnull=True).exclude(credit_card_number="")
        elif credit_card_filter == "No":
            users = CustomUser.objects.filter(
                credit_card_number__isnull=True) | CustomUser.objects.filter(credit_card_number="")
        else:
            users = CustomUser.objects.all()

        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)
