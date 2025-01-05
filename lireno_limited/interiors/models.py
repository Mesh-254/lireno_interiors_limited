import uuid
from django.db import models
from decimal import Decimal

class Category(models.Model):
    category_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=255, null=False)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name


class Supplier(models.Model):
    supplier_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    supplier_name = models.CharField(max_length=255, null=False)
    supplier_email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=False, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.supplier_name


class Stock(models.Model):
    stock_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, null=False)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.quantity}"


class PurchaseItem(models.Model):
    purchase_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='purchases')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, related_name='purchases')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    perprice = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    totalprice = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.totalprice = self.quantity * self.perprice
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Purchase {self.purchase_id}"


class SaleItem(models.Model):
    sale_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='sales')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    perprice = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    totalprice = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        discounted_price = self.perprice * (Decimal(1) - self.discount / Decimal(100))
        self.totalprice = self.quantity * discounted_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Sale {self.sale_id}"
