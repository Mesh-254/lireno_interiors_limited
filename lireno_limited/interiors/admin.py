from django.contrib import admin
from .models import Category, Product, Supplier, Stock, PurchaseItem, SaleItem

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Supplier)
admin.site.register(Stock)
admin.site.register(PurchaseItem)
admin.site.register(SaleItem)