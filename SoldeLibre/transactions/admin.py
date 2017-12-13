from django.contrib import admin
from transactions.models import PaymentMethod, Transaction


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ("name", "icon", "is_active")
    list_filter = ("is_active",)
    list_search = ("name", "abbreviation")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "amount", "method", "updated_by")
    list_filter = ("user", "date", "method", "updated_by")
    list_search = ("description",)
