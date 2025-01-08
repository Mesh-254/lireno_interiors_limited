from django.urls import path, include
from interiors import views



urlpatterns = [
    path('categories/list/', views.CategoryList.as_view(), name='category-list'),
    path('categories/<str:pk>/', views.CategoryDetail.as_view(), name='category-detail'),

    path('products/list/', views.ProductList.as_view(), name='product-list'),
    path('products/<str:pk>/', views.ProductDetail.as_view(), name='product-detail'),

    path('suppliers/list/', views.SupplierList.as_view(), name='supplier-list'),
    path('suppliers/<str:pk>/', views.SupplierDetail.as_view(), name='supplier-detail'),

    path('stocks/list/', views.StockList.as_view(), name='stock-list'),
    path('stocks/<str:pk>/', views.StockDetail.as_view(), name='stock-detail'),

    path('purchases/list/', views.PurchaseList.as_view(), name='purchase-list'),
    path('purchases/<str:pk>/', views.PurchaseDetail.as_view(), name='purchase-detail'),

    path('sales/list/', views.SaleList.as_view(), name='sale-list'),
    path('sales/<str:pk>/', views.SaleDetail.as_view(), name='sale-detail'),

    path('users/list/', views.UserList.as_view(), name='user-list'),
    path('users/<str:pk>/', views.UserDetail.as_view(), name='user-detail'),

    path('auth/', include('rest_framework.urls')),
]