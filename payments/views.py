from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PaymentSerializer


class PaymentView(APIView):

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)

        if serializer.is_valid():
            return Response({"detail": "Payment successful."}, status=status.HTTP_201_CREATED)

        if hasattr(serializer, "http_error"):
            return Response(serializer.errors, status=serializer.http_error)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
