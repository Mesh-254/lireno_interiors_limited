from rest_framework import serializers
from .models import Category, Product, Supplier, Stock, PurchaseItem, SaleItem
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):

    products = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        format='html',
        many=True,
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'products']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'], validated_data['email'], validated_data['password'])
        return user


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    products = serializers.HyperlinkedRelatedField(
        view_name='product-detail',
        format='html',
        many=True,
        read_only=True
    )

    class Meta:
        model = Category
        fields = ['category_id', 'category_name', 'description', 'products']

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.category_name = validated_data.get(
            'category_name', instance.category_name)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.save()
        return instance


class ProductSerializer(serializers.HyperlinkedModelSerializer):

    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=True
    )

    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
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


class SupplierSerializer(serializers.HyperlinkedModelSerializer):
    purchases = serializers.HyperlinkedIdentityField(
        view_name='purchase-detail',
        format='html',
        many=True,
        read_only=True
    )

    class Meta:
        model = Supplier
        fields = '__all__'

    def create(self, validated_data):
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

    def validatePhone_number(self, phone_number):
        if len(phone_number) < 10:
            raise serializers.ValidationError(
                "Phone number must be at least 10 digits.")
        return phone_number


class StockSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

    def create(self, validated_data):
        return Stock.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance


class PurchaseItemSerializer(serializers.HyperlinkedModelSerializer):

    stock = serializers.PrimaryKeyRelatedField(
        queryset=Stock.objects.all(),
        required=True

    )

    supplier = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all(),
        required=False
    )

    purchase_url = serializers.HyperlinkedIdentityField(
        view_name='purchase-detail',
        format='html',
        read_only=True
    )

    class Meta:
        model = PurchaseItem
        fields = ['purchase_url','purchase_id', 'stock',
                  'supplier', 'quantity', 'perprice', 'totalprice', 'date']
        extra_kwargs = {
            'totalprice': {'read_only': True}
        }

    def create(self, validated_data):
        return PurchaseItem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.stock = validated_data.get('stock', instance.stock)
        instance.supplier = validated_data.get('supplier', instance.supplier)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.perprice = validated_data.get('perprice', instance.perprice)
        instance.save()  # totalprice is auto-calculated in the model's save()
        return instance


class SaleItemSerializer(serializers.HyperlinkedModelSerializer):
    
    stock = serializers.PrimaryKeyRelatedField(
        queryset=Stock.objects.all(),
        required=True
    )

    sale_url = serializers.HyperlinkedIdentityField(
        view_name='sale-detail',
        format='html',
        read_only=True
    )

    class Meta:
        model = SaleItem
        fields = ['sale_url','sale_id', 'stock', 'quantity', 'perprice', 'discount', 'date']
        extra_kwargs = {
            'totalprice': {'read_only': True}
        }
        

    def create(self, validated_data):
        return SaleItem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.stock = validated_data.get('stock', instance.stock)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.perprice = validated_data.get('perprice', instance.perprice)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.save()  # totalprice is auto-calculated in the model's save()
        return instance
