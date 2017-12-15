from rest_framework import routers
import transactions.views as views

router = routers.DefaultRouter()
router.register(
    r'category',
    views.CategoryViewSet,
    base_name='category',
)
router.register(
    r'accounts',
    views.AccountViewSet,
    base_name='accounts'
)
router.register(
    r'transactions',
    views.TransactionViewSet,
    base_name='transaction'
)

urlpatterns = router.urls
