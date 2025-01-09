from django.urls import path, include
from interiors import views
from rest_framework.routers import DefaultRouter


# Create a router and register our ViewSets with it.
router = DefaultRouter()

router.register(r'users', views.UserViewSet, basename='user')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'suppliers', views.SupplierViewSet, basename='supplier')
router.register(r'stocks', views.StockViewSet, basename='stock')
router.register(r'purchases', views.PurchaseItemViewSet, basename='purchase')
router.register(r'sales', views.SaLeItemViewSet, basename='sale')


urlpatterns = [
    path('', include(router.urls)),
]