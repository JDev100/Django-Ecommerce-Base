
from django.db import models
from django.contrib.auth.models import User
from django.forms import BooleanField, ImageField

# Create your models here.

class Customer(models.Model):
    """Basically like Django's User. Contains name and email and one to one relationship
    with a Django User"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    """Model for product data. Contains name, price, image, and boolean for 
    digital product status"""
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    image = models.ImageField(null=True, blank=True)
    digital = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url                
        
class Order(models.Model):
    """
    Model for an order. Has relationship with a Customer. 
    Contains data for date ordered, completion status, and transaction id 
    """
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    @property
    def get_cart_total(self):
        orderItems = self.orderitem_set.all()
        total = sum ([item.get_total for item in orderItems])
        return total

    @property
    def get_total_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])    
        return total

    @property
    def shipping(self):
        shipping = False
        orderItems = self.orderitem_set.all()
        for i in orderItems:
            if i.product.digital == False:
                shipping = True
        return shipping 

    def __str__(self) -> str:
        return str(self.id)



class OrderItem(models.Model):
    """Order items stocked in an Order for current Customer.
    Contains product, quantity and date added"""
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)    
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    """Basic model for shipping info. Contains
    Customer, Order, address, city, state, zipcode,
    and date added"""
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address