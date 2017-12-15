from rest_framework import viewsets, mixins
from transactions.models import Account, Category, Transaction
from transactions.serializers import AccountSerializer
from transactions.serializers import TransactionSerializer
from transactions.serializers import CategorySerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Views for Category objects.

    :methods: GET

    """
    queryset = Category.objects.filter(
        is_active=True)
    serializer_class = CategorySerializer
    pagination_class = None


class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Views for Account objects.

    :methods: GET

    """
    queryset = Account.objects.filter(
        is_active=True)
    serializer_class = AccountSerializer
    pagination_class = None


class TransactionViewSet(viewsets.ModelViewSet):
    """
    Views for Transaction objects.

    :methods: GET, POST, PATCH

    """

    serializer_class = TransactionSerializer

    def get_queryset(self):
        if self.request.user.has_perm("transaction.view"):
            return Transaction.objects.all()
        else:
            return Transaction.objects.filter(
                user=self.request.user,
            )
