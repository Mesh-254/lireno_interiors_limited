from django.urls import path
from interiors import views


urlpatterns = [
    path('categories/', views.CategoryList.as_view()),
    path('categories/<str:pk>/', views.CategoryDetail.as_view()),


    path('products/list/', views.ProductList.as_view()),
    path('products/create/', views.ProductCreate.as_view()),
    path('products/<str:pk>/', views.ProductDetail.as_view()),

    path('suppliers/list/', views.SupplierList.as_view()),
    path('suppliers/<str:pk>/', views.SupplierDetail.as_view()),

    path('stocks/list/', views.StockList.as_view()),
    path('stocks/<str:pk>/', views.StockDetail.as_view()),

    path('purchases/list/', views.PurchaseList.as_view()),
    path('purchases/<str:pk>/', views.PurchaseDetail.as_view()),

    path('sales/list/', views.SaleList.as_view()),
    path('sales/<str:pk>/', views.SaleDetail.as_view()),

]