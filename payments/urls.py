from django.urls import path

from .views import CurrencyView, PaymentsView

urlpatterns = [
    path('', PaymentsView.as_view(), name="payments"),
    path('currency/', CurrencyView.as_view(), name="currencies"),
]
