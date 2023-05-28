from django.shortcuts import render

from rest_framework import filters, generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Currency, Payments
from .serializers import CurrencyModelSerializer, PaymentsModelSerializer


class CurrencyView(APIView):
    """
    Handles API endpoints for Currency model
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        currencies = Currency.objects.all()
        serializer = CurrencyModelSerializer(currencies, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = CurrencyModelSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentsView(APIView):
    """
    Handles API endpoints for Payments model
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        queryset = Payments.objects.all()
        reference_code_param = request.GET.get("reference_code")
        currency_param = request.GET.get("currency")

        if reference_code_param:
            queryset = queryset.filter(reference_code=reference_code_param)

        if currency_param:
            queryset = queryset.filter(currency__code__iexact=currency_param)

        serializer = PaymentsModelSerializer(queryset, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = PaymentsModelSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.create_payments(request, request.user))
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
