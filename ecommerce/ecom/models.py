from django.db import models
from django . utils import timezone

# Create your models here.

class Login(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
    role = models.CharField(max_length=10)   

class Registration(models.Model):
    name = models.CharField(max_length=50)
    email =models.EmailField(unique=True)
    number = models.CharField(max_length=10)
    role = models.CharField(max_length=10)
    password = models.CharField(max_length=20)

    login_id = models.OneToOneField(Login, on_delete=models.CASCADE)


class Product(models.Model):
    product_name = models.CharField(max_length=50)
    price = models.IntegerField()
    image = models.ImageField(upload_to='image')
    category = models.CharField(max_length=50)


class ReviewProduct(models.Model):
    product_id = models.CharField(max_length=10)
    user_id = models.CharField(max_length=10)
    product_name = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50)
    time = models.DateTimeField(default=timezone.now,auto_created = True)
    description = models.TextField()


class Cart(models.Model):
    product_id = models.CharField(max_length=10)
    user_id = models.CharField(max_length=10)
    product_name = models.CharField(max_length=50)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    image = models.ImageField(upload_to='image',default='image')
    cart_status = models.IntegerField(default=1)


class WishList(models.Model):
    product_id = models.CharField(max_length=10)
    user_id = models.CharField(max_length=10)
    product_name = models.CharField(max_length=50)
    price = models.IntegerField()
    image = models.ImageField(upload_to='image')    


class Address(models.Model):
    user_id = models.OneToOneField(Login, on_delete=models.CASCADE)  

    name = models.CharField(max_length=50)
    number = models.CharField(max_length=10)
    pincode = models.CharField(max_length=6)
    locality = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)


class Order(models.Model):
    product_id = models.CharField(max_length=10)
    user_id = models.CharField(max_length=10)
    product_name = models.CharField(max_length=50)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    image = models.ImageField(upload_to='image',default='image')
    date = models.DateTimeField(auto_created=True, default=timezone.now)
    order_status = models.CharField(max_length=20,default='pending')


class CardPayment(models,Model):
    user_id =
    payment_mode =
    card



 
