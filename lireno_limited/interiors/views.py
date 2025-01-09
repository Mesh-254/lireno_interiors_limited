# Importing necessary modules from Django and DRF (Django REST Framework)
from rest_framework.response import Response
# Importing all models (Category, Product, Supplier, Stock, etc.)
from .models import *
from .serializers import *  # Importing all serializers for different models
# Exception for validation errors
from rest_framework.exceptions import ValidationError
# Importing the User model for authentication
from django.contrib.auth.models import User
# Importing viewset and permission classes from DRF
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view  # For defining API views in DRF
# For reversing view names to generate URLs
from rest_framework.reverse import reverse


# ViewSet for managing User data with read-only access
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list`
    and `retrieve` actions for users.
    """
    # Queryset to fetch all users from the User model
    queryset = User.objects.all()
    # Serializer used for converting User objects into JSON data
    serializer_class = UserSerializer
    # Permission that ensures only authenticated users can access this endpoint
    permission_classes = [permissions.IsAuthenticated]


# ViewSet for managing Category data with full CRUD actions
class CategoryViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`,
    `retrieve`, `update` and `destroy` actions for categories.
    """
    queryset = Category.objects.all().order_by(
        'category_name')  # Queryset to fetch all category objects
    serializer_class = CategorySerializer  # Serializer used for Category model
    # Permission for authenticated users or read-only access for others
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# ViewSet for managing Product data with full CRUD actions
class ProductViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for products.
    """
    queryset = Product.objects.all().order_by(
        'created_at')  # Query all products ordered by 'created_at'
    # Serializer for handling Product objects
    serializer_class = ProductSerializer
    # Permission for both authenticated users and read-only access
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Override perform_create to handle custom behavior during object creation
    def perform_create(self, serializer):
        # Get product image from request
        image = self.request.FILES.get('image')
        created_by = self.request.user  # Get currently authenticated user
        category_id = self.request.data.get(
            'category')  # Get category ID from request

        # Handling exception if category does not exist
        try:
            category = Category.objects.get(
                category_id=category_id)  # Fetch the category
        except Category.DoesNotExist:
            raise ValidationError(
                # Raise error if not found
                {"category": "The specified category does not exist."})

        # Save the product with its associated information
        serializer.save(category=category, image=image, created_by=created_by)


# ViewSet for managing Supplier data with full CRUD actions
class SupplierViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for suppliers.
    """
    queryset = Supplier.objects.all()  # Query all Supplier objects
    serializer_class = SupplierSerializer  # Serializer for Supplier model
    # Only authenticated users can perform CRUD actions
    permission_classes = [permissions.IsAuthenticated]

    # Override perform_create for additional logic (if needed)
    def perform_create(self, serializer):
        serializer.save()  # Save the Supplier instance after validation


# ViewSet for managing Stock data with full CRUD actions
class StockViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`,
    `retrieve`, `update` and `destroy` actions for stocks.
    """
    queryset = Stock.objects.all()  # Fetch all stock records
    serializer_class = StockSerializer  # Stock serializer class
    # Only authenticated users have access
    permission_classes = [permissions.IsAuthenticated]


# ViewSet for managing Purchase Item data with full CRUD actions
class PurchaseItemViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for purchase items.
    """
    queryset = PurchaseItem.objects.all().order_by(
        '-date')  # Order purchases by date in descending order
    # Serializer class for PurchaseItem model
    serializer_class = PurchaseItemSerializer
    # Only authenticated users can perform CRUD actions
    permission_classes = [permissions.IsAuthenticated]

    # Override the default 'create' behavior to include custom logic
    def perform_create(self, serializer):
        # Retrieve stock ID from request
        stock_id = self.request.data.get('stock')
        # Retrieve supplier ID from request
        supplier_id = self.request.data.get('supplier')
        # Retrieve quantity from request
        quantity = self.request.data.get('quantity')

        try:
            stock = Stock.objects.get(stock_id=stock_id)  # Fetch stock by ID
            supplier = Supplier.objects.get(
                supplier_id=supplier_id)  # Fetch supplier by ID
        except Stock.DoesNotExist:
            raise ValidationError(
                # If stock does not exist, raise error
                {"stock": "The specified stock does not exist."})
        except Supplier.DoesNotExist:
            raise ValidationError(
                # If supplier does not exist, raise error
                {"supplier": "The specified supplier does not exist."})

        # Validate that quantity is greater than 0
        if int(quantity) < 1:
            raise ValidationError(
                {"quantity": "The quantity must be greater than 0."})

        # Update stock quantity before saving the purchase item
        stock.quantity += int(quantity)
        stock.save()

        # Save the PurchaseItem instance after setting related fields
        serializer.save(stock=stock, supplier=supplier)

    # Override the 'update' method for handling
    # stock quantity changes when purchase is updated
    def perform_update(self, serializer):
        # Retrieve stock from the request
        stock = self.request.data.get('stock')
        # Retrieve updated quantity from the request
        quantity = self.request.data.get('quantity')
        supplier = self.request.data.get(
            'supplier')  # Retrieve updated supplier

        try:
            stock = Stock.objects.get(stock_id=stock)  # Fetch stock by ID
            supplier = Supplier.objects.get(
                supplier_id=supplier)  # Fetch supplier by ID
        except Stock.DoesNotExist:
            raise ValidationError(
                {"stock": "The specified stock does not exist."})
        except Supplier.DoesNotExist:
            raise ValidationError(
                {"supplier": "The specified supplier does not exist."})

        # Update the stock quantity after considering
        # the existing quantity in PurchaseItem
        # Get the existing PurchaseItem object
        purchase_item = self.get_object()
        # Get the old quantity in the stock
        old_quantity = purchase_item.quantity

        # Revert the previous quantity in the stock
        # before updating to the new value
        stock.quantity -= old_quantity
        stock.save()

        stock.quantity += int(quantity)
        stock.save()

        # Save the updated PurchaseItem instance
        serializer.save(stock=stock, supplier=supplier)

    # Override the 'destroy' method
    #  to adjust the stock quantity when a purchase is deleted
    def perform_destroy(self, instance):
        stock = instance.stock  # Retrieve the related stock
        # Update the stock quantity by subtracting the purchased quantity
        stock.quantity -= instance.quantity
        stock.save()

        # Perform the default destroy action
        super().perform_destroy(instance)


# ViewSet for managing SaleItem data with full CRUD actions
class SaLeItemViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for sale items.
    """
    queryset = SaleItem.objects.all().order_by(
        '-date')  # Order sale items by date in descending order
    # Serializer class for SaleItem model
    serializer_class = SaleItemSerializer
    # Only authenticated users can access
    permission_classes = [permissions.IsAuthenticated]

    # Custom 'create' method for SaleItem to update stock and handle sales
    def perform_create(self, serializer):
        stock = self.request.data.get('stock')  # Retrieve the stock ID
        # Retrieve quantity of item to be sold
        quantity = self.request.data.get('quantity')

        try:
            # Fetch the stock by its ID
            stock = Stock.objects.get(stock_id=stock)
        except Stock.DoesNotExist:
            raise ValidationError(
                {"stock": "The specified stock does not exist."})

        # Validate that the quantity is not less than 1
        if int(quantity) < 1:
            raise ValidationError(
                {"quantity": "The quantity must be greater than 0."})

        # Ensure that the sale doesn't exceed available stock quantity
        if Decimal(quantity) > stock.quantity:
            raise ValidationError(
                {"quantity": f"The sale exceeds the current stock quantity of {stock.quantity}."})

        # Decrease the stock quantity based on the sold quantity
        stock.quantity -= int(quantity)
        stock.save()

        # Save the sale item after adjusting the stock
        serializer.save(stock=stock)

    # 'update' method for SaleItem to handle updates and stock adjustments
    def perform_update(self, serializer):
        stock = self.request.data.get('stock')  # Retrieve the stock ID
        # Retrieve updated quantity for sale
        quantity = self.request.data.get('quantity')

        try:
            stock = Stock.objects.get(stock_id=stock)  # Fetch stock by ID
        except Stock.DoesNotExist:
            raise ValidationError(
                {"stock": "The specified stock does not exist."})

        # Fetch the existing SaleItem and adjust stock quantity accordingly
        sale_item = self.get_object()  # Get the existing SaleItem
        old_quantity = sale_item.quantity  # Get the old sale quantity

        # Revert the previous sale quantity before applying the new quantity
        stock.quantity += old_quantity
        stock.save()

        # Subtract the updated sale quantity from the stock
        stock.quantity -= int(quantity)
        stock.save()

        # Save the updated SaleItem object
        serializer.save(stock=stock)

    # Custom 'destroy' method for SaleItem to update stock after deletion
    def perform_destroy(self, instance):
        # Retrieve the related stock for the SaleItem
        stock = instance.stock
        # Add back the quantity removed by the sale
        stock.quantity += instance.quantity
        stock.save()

        # Perform the default destroy action for SaleItem
        super().perform_destroy(instance)
