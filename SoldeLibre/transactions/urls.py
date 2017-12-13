from rest_framework import routers
import transactions.views as views

router = routers.DefaultRouter()
router.register(
    r'payment_methods',
    views.PaymentMethodViewSet,
    base_name='payment_methods'
)
router.register(
    r'transactions',
    views.TransactionViewSet,
    base_name='transaction'
)

urlpatterns = router.urls
