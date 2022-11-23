from rest_framework.routers import DefaultRouter

from .views import OrderViewSet

router = DefaultRouter()
router.register('order', OrderViewSet, 'orders')


urlpatterns = []

urlpatterns += router.urls