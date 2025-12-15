from functools import lru_cache
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.context_processors import request
from phonenumber_field.modelfields import PhoneNumberField

class UserProfile(AbstractUser):
    phone_number = PhoneNumberField()
    RoleChoices = (
    ('client', 'client'),
    ('owner', 'owner'),
    ('courier', 'courier'),
    )
    role = models.CharField(max_length=20, choices=RoleChoices, default='client')
    date_registered = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'



class Category(models.Model):
    category_name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.category_name

class Store(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    store_name = models.CharField(max_length=20, unique=True)
    store_photo = models.ImageField(upload_to="store_photos/")
    description = models.TextField()
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.store_name

    def get_avg_rating(self ):
        reviews = self.store_reviews.all()
        if reviews.exists():
            return round(sum([i.rating for i in reviews]) / reviews.count(),1)
        return 0

    def get_count_people(self):
        ratings = self.store_reviews.all()
        if ratings.exists():
            if ratings.count() > 3:
                return '3+'
            return ratings.count()
        return 0

    def get_avg_procent(self):
        ratings = self.store_reviews.all()
        count_person = 0
        if ratings.exists():
            for i in ratings:
                if i.rating > 3:
                    count_person += 1
                continue
            return f'{round((count_person * 100) / ratings.count(), 1)}%'

        return '0%'


class Contact(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_contact')
    contact_name = models.CharField(max_length=20)
    contact_number = PhoneNumberField()

    def __str__(self):
        return f'{self.contact_name} {self.contact_number}'

class Address(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_address')
    address_name = models.CharField(max_length=20)

    def __str__(self):
        return self.address_name

class StoreMenu(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='StoreMenu')
    menu_name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.menu_name


class Product(models.Model):
    store = models.ForeignKey(StoreMenu, on_delete=models.CASCADE, related_name='storeproduct')
    product_name = models.CharField(max_length=50)
    product_image = models.ImageField(upload_to="products_photos/")
    product_description = models.TextField()
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.product_name

class Order(models.Model):
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='order_client')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    StatusChoices = (
    ('pending', 'pending'),
    ('canceled', 'cancled'),
    ('delivered', 'delivered'),
    )
    status = models.CharField(max_length=20, choices=StatusChoices, default='pending')
    delivery_address = models.TextField()
    courier = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='order_courier')
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.client} {self.product} {self.status}'

class CourierProduct(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    current_orders = models.ForeignKey(Order, on_delete=models.CASCADE)
    CourierStatusChoices = (
    ('busy', 'busy'),
    ('available', 'available'),
    )
    courier_status = models.CharField(max_length=20, choices=CourierStatusChoices)

    def __str__(self):
        return f'{self.user},{self.courier_status}'

class Review(models.Model):
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='review_client', )
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True, related_name='store_reviews')
    courier = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='review_courier', null=True, blank=True)
    rating = models.PositiveIntegerField(choices=[(i,str(i)) for i in range(1, 6)])
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.client},  {self.rating}'