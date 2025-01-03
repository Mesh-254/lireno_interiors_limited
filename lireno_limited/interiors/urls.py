from django.urls import path
from interiors import views


urlpatterns = [
    path('categories/', views.category_list),
    path('categories/<str:pk>/', views.category_detail),
]