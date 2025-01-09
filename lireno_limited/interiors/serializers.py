# Import necessary modules and models
from rest_framework import serializers
from .models import Category, Product, Supplier, Stock, PurchaseItem, SaleItem
from django.contrib.auth.models import User

# Serializer for User Model


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # Provides hyperlinks to products associated with the user
    products = serializers.HyperlinkedIdentityField(
        view_name='product-detail',  # Refers to the detail view for products
        format='html',              # Specifies format as HTML
        many=True,                  # Indicates multiple related products
    )

    class Meta:
        model = User  # Specifies the model to serialize
        fields = ['id', 'username', 'email', 'password',
                  'products']  # Defines serialized fields
        # Ensures password is write-only
        extra_kwargs = {'password': {'write_only': True}}

    # Overriding create method for handling user creation
    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )
        return user

# Serializer for Category Model


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    # Hyperlinked relation to related products
    products = serializers.HyperlinkedRelatedField(
        view_name='product-detail',  # Refers to product detail URLs
        format='html',               # Specifies format as HTML
        many=True,                   # Indicates multiple related products
        read_only=True               # Prevent modification through serializer
    )

    # Provides hyperlink to the category itself
    category_url = serializers.HyperlinkedIdentityField(
        view_name='category-detail',
        format='html'
    )

    class Meta:
        model = Category  # Specifies the model to serialize
        fields = ['category_url', 'category_id',
                  'category_name', 'description', 'products']

    # Overriding create and update methods
    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.category_name = validated_data.get(
            'category_name', instance.category_name)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.save()
        return instance

# Serializer for Product Model


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    # Relates product to a specific category using primary keys
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),  # Retrieves all categories
        required=True                    # Specifies category is mandatory
    )

    # Field showing the user who created the product
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Product  # Specifies the model to serialize
        fields = '__all__'  # Serializes all fields

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Updates product details
        instance.product_name = validated_data.get(
            'product_name', instance.product_name)
        instance.image = validated_data.get('image', instance.image)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.category = validated_data.get('category', instance.category)
        instance.is_active = validated_data.get(
            'is_active', instance.is_active)
        instance.save()
        return instance

# Serializer for Supplier Model


class SupplierSerializer(serializers.HyperlinkedModelSerializer):
    # Provides links to purchase items related to the supplier
    purchases = serializers.HyperlinkedIdentityField(
        view_name='purchase-detail',
        format='html',
        many=True,
        read_only=True
    )

    class Meta:
        model = Supplier  # Specifies the model to serialize
        fields = '__all__'  # Serializes all fields

    # Custom phone number validation method
    def validatePhone_number(self, phone_number):
        if len(phone_number) < 10:
            raise serializers.ValidationError(
                "Phone number must be at least 10 digits.")
        return phone_number

    # Methods for creating and updating suppliers
    def create(self, validated_data):
        validated_data['phone_number'] = self.validatePhone_number(
            validated_data.get('phone_number'))
        return Supplier.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.supplier_name = validated_data.get(
            'supplier_name', instance.supplier_name)
        instance.supplier_email = validated_data.get(
            'supplier_email', instance.supplier_email)
        instance.phone_number = validated_data.get(
            'phone_number', instance.phone_number)
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        return instance

# Serializer for Stock Model


class StockSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Stock  # Specifies the model to serialize
        fields = '__all__'  # Serializes all fields

    def create(self, validated_data):
        return Stock.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Updates stock details
        instance.name = validated_data.get('name', instance.name)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance

# Serializer for PurchaseItem Model


class PurchaseItemSerializer(serializers.HyperlinkedModelSerializer):
    stock = serializers.PrimaryKeyRelatedField(
        queryset=Stock.objects.all(),  # Specifies related stock
        required=True
    )

    supplier = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all(),  # Specifies related supplier
        required=False
    )

    purchase_url = serializers.HyperlinkedIdentityField(
        view_name='purchase-detail',
        format='html',
        read_only=True  # Cannot be modified
    )

    class Meta:
        model = PurchaseItem  # Specifies the model to serialize
        fields = ['purchase_url', 'purchase_id', 'stock',
                  'supplier', 'quantity', 'perprice', 'totalprice', 'date']
        extra_kwargs = {
            'totalprice': {'read_only': True}  # Automatically calculated
        }

    def create(self, validated_data):
        return PurchaseItem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Updates purchase details
        instance.stock = validated_data.get('stock', instance.stock)
        instance.supplier = validated_data.get('supplier', instance.supplier)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.perprice = validated_data.get('perprice', instance.perprice)
        instance.save()
        return instance

# Serializer for SaleItem Model


class SaleItemSerializer(serializers.HyperlinkedModelSerializer):
    stock = serializers.PrimaryKeyRelatedField(
        queryset=Stock.objects.all(),  # Specifies related stock
        required=True
    )

    sale_url = serializers.HyperlinkedIdentityField(
        view_name='sale-detail',
        format='html',
        read_only=True  # Cannot be modified
    )

    class Meta:
        model = SaleItem  # Specifies the model to serialize
        fields = ['sale_url', 'sale_id', 'stock', 'quantity',
                  'perprice', 'discount', 'date']
        extra_kwargs = {
            'totalprice': {'read_only': True}  # Automatically calculated
        }

    def create(self, validated_data):
        return SaleItem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Updates sale details
        instance.stock = validated_data.get('stock', instance.stock)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.perprice = validated_data.get('perprice', instance.perprice)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.save()
        return instance
