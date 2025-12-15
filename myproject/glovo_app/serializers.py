from rest_framework import serializers
from .admin import (UserProfile, Category, Store, Contact, Address, StoreMenu,
                    Product, Order, CourierProduct,Review)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'age',
                  'phone_number', 'status']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name']


class UserProfileOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name']

class UserProfileClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name']

class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserProfileStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name']

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','category_name']

class CategoryNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']

class StoreListSerializer(serializers.ModelSerializer):
    created_date = serializers.DateField(format='%m/%d/%Y')
    class Meta:
        model = Store
        fields = ['id','store_name', 'store_photo','get_avg_rating','get_count_people','get_avg_procent','created_date']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating

    def get_count_people(self, obj):
        return obj.get_count_people()

    def get_avg_procent(self, obj):
        return obj.get_avg_procent()

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','product_name', 'product_image', 'quantity']


class StoreCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'

class StoreMenuListSerializer(serializers.ModelSerializer):
    store_product = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = StoreMenu
        fields = ['id','menu_name',  'store_product']



class StoreMenuDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = StoreMenu
        fields = ['menu_name',]


class StoreCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['store_name', 'store_photo', ]

class CategoryDetailSerializer(serializers.ModelSerializer):
    category = StoreCategorySerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = '__all__'



class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [ 'contact_name', 'contact_number']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['address_name']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class ProductOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_name',]

class OrderStatusSerializer(serializers.ModelSerializer):
    product = ProductOrderSerializer()
    client = UserProfileOrderSerializer()
    class Meta:
        model = Order
        fields = ['id', 'product', 'client', 'status']


class CourierProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourierProduct
        fields = '__all__'

class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    client = UserProfileClientSerializer()
    class Meta:
        model = Review
        fields = ['id','client','courier','rating', 'text', 'created_date']




class StoreDetailSerializer(serializers.ModelSerializer):
    created_date = serializers.DateField(format='%m/%d/%Y')
    category = CategoryNameSerializer()
    StoreMenu = StoreMenuListSerializer(many=True, read_only=True)
    store_contact = ContactSerializer(many=True, read_only=True)
    store_address = AddressSerializer(many=True, read_only=True)
    store_review = ReviewSerializer(many=True, read_only=True)
    owner = UserProfileStoreSerializer()
    class Meta:
        model = Store
        fields = ['store_name', 'store_photo','category', 'description','StoreMenu', 'owner','store_review','created_date','store_contact','store_address',]