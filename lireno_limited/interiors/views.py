from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse



@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'categories': reverse('category-list', request=request, format=format),
        'products': reverse('product-list', request=request, format=format),
        'suppliers': reverse('supplier-list', request=request, format=format),
        'stocks': reverse('stock-list', request=request, format=format),
        'purchases': reverse('purchase-list', request=request, format=format),
        'sales': reverse('sale-list', request=request, format=format),
    })



class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]



class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by('created_at')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    def perform_create(self, serializer):
        image = self.request.FILES.get('image')
        created_by = self.request.user
        category_id = self.request.data.get('category')

        try:
            category = Category.objects.get(category_id=category_id)

        except Category.DoesNotExist:

            raise ValidationError(
                {"category": "The specified category does not exist."})

        serializer.save(category=category, image=image, created_by=created_by)


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SupplierList(generics.ListCreateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]


    def perform_create(self, serializer):
        serializer.save()


class SupplierDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]



class StockList(generics.ListCreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [permissions.IsAuthenticated]


class StockDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [permissions.IsAuthenticated]


class PurchaseList(generics.ListCreateAPIView):
    queryset = PurchaseItem.objects.all()
    serializer_class = PurchaseItemSerializer
    permission_classes = [permissions.IsAuthenticated]

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
    permission_classes = [permissions.IsAuthenticated]

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


class SaleList(generics.ListCreateAPIView):
    queryset = SaleItem.objects.all().order_by('stock_id')
    serializer_class = SaleItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        stock = self.request.data.get('stock')
        quantity = self.request.data.get('quantity')

        try:
            stock = Stock.objects.get(stock_id=stock)

        except Stock.DoesNotExist:
            raise ValidationError(
                {"stock": "The specified stock does not exist."})

        if int(quantity) < 1:
            raise ValidationError(
                {"quantity": "The quantity must be greater than 0."})
        
        if Decimal(quantity) > stock.quantity:
            raise ValidationError(
                {"quantity": f"The sale exceeds the current stock quantity of {stock.quantity}."})

        stock.quantity -= int(quantity)
        stock.save()

        serializer.save(stock=stock)


class SaleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SaleItem.objects.all()
    serializer_class = SaleItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        stock = self.request.data.get('stock')
        quantity = self.request.data.get('quantity')

        try:
            stock = Stock.objects.get(stock_id=stock)

        except Stock.DoesNotExist:
            raise ValidationError(
                {"stock": "The specified stock does not exist."})

        # Fetch the existing purchase item and revert the stock quantity before adding the new quantity
        sale_item = self.get_object()  # Get the PurchaseItem being updated
        # Get the old quantity that was in the stock
        old_quantity = sale_item.quantity

        # Revert the stock quantity by adding the old quantity
        stock.quantity += old_quantity
        stock.save()

        stock.quantity -= int(quantity)
        stock.save()

        serializer.save(stock=stock)

    def perform_destroy(self, instance):
        stock = instance.stock

        stock.quantity += instance.quantity
        stock.save()

        # Call the original `perform_destroy` to delete the PurchaseItem
        super().perform_destroy(instance)
