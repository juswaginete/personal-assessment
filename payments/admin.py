from django.contrib import admin

from .models import Payments

class PaymentsAdmin(admin.ModelAdmin):
    class Meta:
        model = Payments

admin.site.register(Payments, PaymentsAdmin)
