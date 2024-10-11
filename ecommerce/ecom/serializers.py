from rest_framework import serializers

from . models import Address, Order, Registration, Login, Product, ReviewProduct, Cart, WishList


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Login     
        fields = '__all__'   

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewProduct  
        fields = '__all__'   

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart 
        fields = '__all__'    

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList    
        fields = '__all__'  
       

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address 
        fields = '__all__'  


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'           
