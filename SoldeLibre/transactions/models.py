from django.db import models

from django.contrib.auth.models import User


class PaymentMethod(models.Model):
    """
    Model of available payment methods.

    """
    name = models.CharField(
        max_length=128,
        help_text="The name of the payment method",
        blank=False, null=False,
    )
    abbreviation = models.CharField(
        max_length=5,
        help_text="The abbreviated name of the payment method",
        blank=False, null=False,
    )
    icon = models.ImageField(
        upload_to="./media/paymentIcons",
        help_text="The icon of the payment method",
        blank=True, null=True
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Set whether the payment method is active or not."
    )

    def __str__(self):
        return self.name


class Transaction(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        help_text="The user the transaction belongs to.",
        blank=False, null=False,
    )
    date = models.DateField(
        help_text="The date of the transaction",
        blank=False, null=False,
    )
    description = models.CharField(
        max_length=256,
        help_text="The description of the transaction",
        blank=False, null=False,
    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=9,      # 1,000,000.00 -- Hopefully that's enough!
        help_text="The amount of the transaction",
        blank=False, null=False,
    )
    method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.PROTECT,
        help_text="The payment method used.",
        blank=False, null=False,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp of when the transaction was created."
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="created_by",
        help_text="The user who created the transaction."
    )
    updated = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp of when the transaction was last updated.",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="updated_by",
        help_text="The user who last updated the transaction",
    )

    permissions = (
        ("view", "Can view all transactions")
    )
