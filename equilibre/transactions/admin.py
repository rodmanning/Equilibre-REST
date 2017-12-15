from django.contrib import admin
from transactions.models import Category, Account, Transaction

admin.site.register(Category)

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("name", "icon", "is_active")
    list_filter = ("is_active",)
    list_search = ("name", "abbreviation")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "amount", "account", "updated_by")
    list_filter = ("user", "date", "account", "updated_by")
    list_search = ("description",)
