from django.contrib import admin
from transactions.models import Account, Balance, Category, Transaction

admin.site.register(Category)
admin.site.register(Balance)

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("name", "icon", "is_active")
    list_filter = ("is_active",)
    list_search = ("name", "abbreviation")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "date", "amount", "account", "tax_deduction", "updated_by")
    list_filter = ("user", "date", "account", "updated_by")
    list_search = ("description",)
    readonly_fields = ("user", "updated", "updated_by", "created", "created_by")
