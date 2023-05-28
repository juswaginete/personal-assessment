from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

optional = {
    'null': True,
    'blank': True,
}


class Currency(models.Model):
    name = models.CharField(max_length=100, **optional)
    code = models.CharField(max_length=100, unique=True, **optional)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Currencies"


class Payments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payment_user")
    currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name="payment_currency",
        **optional
    )
    reference_code = models.CharField(max_length=100, unique=True, **optional)
    amount = models.IntegerField(**optional)
    is_paid = models.BooleanField(default=False)
    paid_date = models.DateField(default=timezone.now)
    created_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.reference_code 

    class Meta:
        verbose_name_plural = "Payments"