from rest_framework import viewsets, mixins
from transactions.models import PaymentMethod, Transaction
from transactions.serializers import PaymentMethodSerializer
from transactions.serializers import TransactionSerializer


class PaymentMethodViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Views for PaymentMethod objects.

    :methods: GET

    """
    queryset = PaymentMethod.objects.filter(
        is_active=True)
    serializer_class = PaymentMethodSerializer
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
