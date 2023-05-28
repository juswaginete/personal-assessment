import re
import sys
import uuid

from datetime import datetime, timedelta

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.settings import settings
from rest_framework.validators import UniqueValidator

from payments.models import Currency, Payments
from payments.utils import is_future_or_passed_datetime


class CurrencyModelSerializer(serializers.ModelSerializer):
    """
    Serializer model class for Currency model
    """

    class Meta:
        model = Currency
        fields = '__all__'


class PaymentsModelSerializer(serializers.ModelSerializer):
    """
    Serializer model class for Payments model
    """

    class Meta:
        model = Payments
        fields = ("currency", "reference_code", "amount")

    def create_payments(self, request, validated_data):
        amount_limit = 5000
        one_day = timedelta(days=1)
        current_datetime = datetime.now()
        tomorrow_datetime = datetime.now() + one_day
        user_object = request.user
        reference_code = str(uuid.uuid4())

        amount = self.data.get("amount")
        currency_id = self.data.get('currency')
        currency = Currency.objects.get(id=currency_id)

        payments_total_amount = Payments.objects.filter(user=user_object).aggregate(sum_amount=Coalesce(Sum('amount'), Value(0)))['sum_amount']

        try:
            if current_datetime.date() != tomorrow_datetime.date() and payments_total_amount < amount_limit:
                payment = Payments(
                    amount=amount,
                    currency=currency,
                    reference_code=reference_code,
                    user=user_object
                )

                payment.save()

                return {
                    "id": payment.id,
                    "user": payment.user.id,
                    "reference_code": payment.reference_code,
                    "amount": payment.amount
                }

            msg = _('Already exceeded the daily total amount limit.')
            raise serializers.ValidationError(msg)
        except Exception as e:
            raise e


