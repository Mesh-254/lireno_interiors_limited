from rest_framework import serializers
from .models import Category, Product, Supplier, Stock, PurchaseItem, SaleItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.category_name = validated_data.get('category_name', instance.category_name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.product_name = validated_data.get('product_name', instance.product_name)
        instance.image = validated_data.get('image', instance.image)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.category = validated_data.get('category', instance.category)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

    def create(self, validated_data):
        return Supplier.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.supplier_name = validated_data.get('supplier_name', instance.supplier_name)
        instance.supplier_email = validated_data.get('supplier_email', instance.supplier_email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        return instance


class StockSerializer(serializers.ModelSerializer):
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


class PurchaseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseItem
        fields = '__all__'

    def create(self, validated_data):
        return PurchaseItem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.stock = validated_data.get('stock', instance.stock)
        instance.supplier = validated_data.get('supplier', instance.supplier)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.perprice = validated_data.get('perprice', instance.perprice)
        instance.save()  # totalprice is auto-calculated in the model's save()
        return instance


class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = '__all__'

    def create(self, validated_data):
        return SaleItem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.stock = validated_data.get('stock', instance.stock)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.perprice = validated_data.get('perprice', instance.perprice)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.save()  # totalprice is auto-calculated in the model's save()
        return instance
