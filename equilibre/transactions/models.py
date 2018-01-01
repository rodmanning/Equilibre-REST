from django.db import models

from django.contrib.auth.models import User


class Category(models.Model):
    """Model of the categories an expense belongs to."""
    name = models.CharField(
        max_length=128,
        help_text="The name of the category",
        blank=False, null=False
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Set whether the category is active or not.",
    )

    def __str__(self):
        return self.name


class Account(models.Model):
    """Model of available payment accounts."""
    name = models.CharField(
        max_length=128,
        help_text="The name of the payment account",
        blank=False, null=False,
    )
    abbreviation = models.CharField(
        max_length=5,
        help_text="The abbreviated name of the payment account",
        blank=False, null=False,
    )
    icon = models.ImageField(
        upload_to="./media/paymentIcons",
        help_text="The icon of the payment account",
        blank=True, null=True
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Set whether the payment account is active or not."
    )
    show_balance = models.BooleanField(
        default=True,
        help_text="Set whether for this account is shown."
    )

    def __str__(self):
        return self.name


class Transaction(models.Model):
    """Model of transactions between accounts."""
    ACTION_CHOICES = (
        (1, "Credit"),
        (-1, "Debit"),
    )

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
    action = models.IntegerField(
        choices=ACTION_CHOICES,
        help_text="Set whether the transaction is a credit or debit.",
        blank=False, null=False,
    )
    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        help_text="The payment account used.",
        blank=False, null=False,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        help_text="The category of the transaction.",
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
    tax_deduction = models.BooleanField(
        default=False,
        help_text="Set whether the transaction is tax deductable."
    )
    permissions = (
        ("view", "Can view all transactions")
    )

    def _update_balances(self, _orig):
        """Update the value of related balances.

        :_orig: A copy of this instance with pre-save values.

        """
        # Calculate how much the balance has changed (including handling null
        # cases), and also check if the account has changed.
        if _orig is not None:
            amount_change = (self.amount * self.action) - (_orig.amount * _orig.action)
            account_changed = self.account != _orig.account
        else:
            amount_change = self.amount * self.action
            account_changed = False

        # Handle cases where the account has changed by reversing-out the
        # original values (e.g. transfer out the amount) and apply the whole
        # value to the new account
        if account_changed is True:
            # Calculate the size of the old amount and update the balance of
            # the old account by *reversing* it (i.e. '-=')
            old_amount = _orig.amount * _orig.action
            old_balance, _ = Balance.objects.get_or_create(account=_orig.account)
            old_balance.value -= old_amount
            old_balance.save()

            # Then update the value of the new account with the whole value of the transaction
            new_balance, _ = Balance.objects.get_or_create(account=self.account)
            new_balance.value += self.amount * self.action
            new_balance.save()

        # Handle cases where the account remains the same by updating the
        # amount of the account currently selected on the transaction
        elif amount_change != 0:
            balance, _ = Balance.objects.get_or_create(
                account=self.account)
            balance.value += amount_change
            balance.save()

    def save(self, *args, **kwargs):
        """Override `save()` method to updated related balances."""
        _orig = type(self).objects.get(pk=self.pk) if self.pk else None
        super(Transaction, self).save(*args, **kwargs)

        # Update the related balances
        self._update_balances(_orig)

        # Call the "real" save() method.
        super().save(*args, **kwargs)


class Balance(models.Model):
    """Model of current balance of an account."""
    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        unique=True,
        help_text="The account the balance has been computed for."
    )
    value = models.DecimalField(
        help_text="The balance of the account.",
        decimal_places=2,
        max_digits=9,      # 1,000,000.00 -- Hopefully that's enough!
        default=0,
        blank=False, null=False,
    )
    updated = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp of when the transaction was last updated.",
        blank=True, null=True
    )

    def __str__(self):
        return self.account.name
