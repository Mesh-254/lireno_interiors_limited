from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.exceptions import ValidationError


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductCreate(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        image = self.request.FILES.get('image')

        category = self.request.data.get('category')

        try:
            category = Category.objects.get(id=category)

        except category.DoesNotExist:

            raise ValidationError(
                {"category": "The specified category does not exist."})

        serializer.save(category=category, image=image)


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    # implement code to allow creation of product with image

    serializer_class = ProductSerializer


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class SupplierList(generics.ListCreateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

    def perform_create(self, serializer):
        serializer.save()


class SupplierDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class StockList(generics.ListCreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class StockDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class PurchaseList(generics.ListCreateAPIView):
    queryset = PurchaseItem.objects.all()
    serializer_class = PurchaseItemSerializer

    def perform_create(self, serializer):
        stock = self.request.data.get('stock')
        supplier = self.request.data.get('supplier')
        quantity = self.request.data.get('quantity')

        try:
            stock = Stock.objects.get(stock_id=stock)
            supplier = Supplier.objects.get(supplier_id=supplier)

        except Stock.DoesNotExist:
            raise ValidationError(
                {"stock": "The specified stock does not exist."})

        except Supplier.DoesNotExist:
            raise ValidationError(
                {"supplier": "The specified supplier does not exist."})

        if int(quantity) < 1:
            raise ValidationError(
                {"quantity": "The quantity must be greater than 0."})

        stock.quantity += int(quantity)
        stock.save()

        serializer.save(stock=stock, supplier=supplier)


class PurchaseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseItem.objects.all()
    serializer_class = PurchaseItemSerializer

    def perform_update(self, serializer):
        stock = self.request.data.get('stock')
        quantity = self.request.data.get('quantity')
        supplier = self.request.data.get('supplier')

        try:
            stock = Stock.objects.get(stock_id=stock)
            supplier = Supplier.objects.get(supplier_id=supplier)

        except Stock.DoesNotExist:
            raise ValidationError(
                {"stock": "The specified stock does not exist."})

          # Fetch the existing purchase item and revert the stock quantity before adding the new quantity
        purchase_item = self.get_object()  # Get the PurchaseItem being updated
        # Get the old quantity that was in the stock
        old_quantity = purchase_item.quantity

        # Revert the stock quantity by removing the old quantity
        stock.quantity -= old_quantity
        stock.save()

        stock.quantity += int(quantity)
        stock.save()

        serializer.save(stock=stock, supplier=supplier)

    def perform_destroy(self, instance):
        stock = instance.stock

        stock.quantity -= instance.quantity
        stock.save()

        # Call the original `perform_destroy` to delete the PurchaseItem
        super().perform_destroy(instance)

