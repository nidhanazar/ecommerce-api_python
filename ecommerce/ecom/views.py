from datetime import datetime
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework .generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q

from . models import Address, Cart, Login, Order, Product, Registration, ReviewProduct, WishList

from  . serializers import AddressSerializer, CartSerializer, LoginSerializer, OrderSerializer, RegisterSerializer, ProductSerializer, ReviewSerializer, WishlistSerializer

# Create your views here.

def index(request):
    return HttpResponse('asdfgh')

class Register_view(GenericAPIView):
    # return the Register Serializer by default, as registration is the main action here
    def get_serializer_class(self):
        return RegisterSerializer
    
    def post(self,request):
    
        login_id = ""
        name = request.data.get('name')
        email = request.data.get('email')
        number = request.data.get('number')
        password = request.data.get('password')
        role = 'user'

        if not name or not email or not number or not password:
            return Response({'message' : 'All fields are required'}, status = status.HTTP_400_BAD_REQUEST,)
        
        if Registration.objects.filter(email=email).exists():
            return Response({'message' : 'Duplicate Emails are not allowed'}, status= status.HTTP_400_BAD_REQUEST,)
        
        elif Registration.objects.filter(number=number).exists():
            return Response({'message' : 'Number already found'}, status= status.HTTP_400_BAD_REQUEST,)
        
        # validate and create login
        login_serializer = LoginSerializer(data = {'email' : email, 'password' : password, 'role' : role})

        if login_serializer.is_valid():
            l = login_serializer.save()
            login_id = l.id 

        else:
            return Response({'message' : 'Login Failed'}, status= status.HTTP_400_BAD_REQUEST,)  



        register_serializer = RegisterSerializer(
            data = {
                'name' : name,
                'email' : email, 
                'number' : number,
                'password' : password, 
                'role' : role, 
                'login_id' :login_id})
        
        if register_serializer.is_valid():
            register_serializer.save()
            return Response({'message': 'Registration Successful'}, status= status.HTTP_200_OK,)
        
        else:
            return Response({'message' : 'Registration Failed'}, status= status.HTTP_400_BAD_REQUEST,)
        

class Login_view(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        logreg = Login.objects.filter(email=email, password=password)
        if(logreg.count() > 0):
            read_serializers = LoginSerializer(logreg, many = True)

            for i in read_serializers.data:
                login_id = i['id']
                role = i['role']

                register_data = Registration.objects.filter(login_id = login_id).values()
                for i in register_data:
                    name = i['name']

            return Response({'data' : {'login_id' : login_id, 'email' : email, 'name' : name, 'password' : password}, 'success' : 1, 'message': 'Logged in Successfully'}, status = status.HTTP_200_OK)
       
        else:
            return Response({'message' : 'Login Failed'}, status= status.HTTP_400_BAD_REQUEST,) 



class All_users_view(GenericAPIView):
    serializer_class = RegisterSerializer

    def get(self,request):
        user = Registration.objects.all()
        if user.count() > 0:
            serializer = RegisterSerializer(user, many= True)
            return Response({'data' : serializer.data, 'message' : 'Data get', 'success' : True}, status=status.HTTP_200_OK)
            
        else:
            return Response({'data' : 'No data available'}, status= status.HTTP_400_BAD_REQUEST)    


class Single_user_view(GenericAPIView):
    serializer_class = RegisterSerializer

    def get(self,request,id):
        user = Registration.objects.get(pk=id)
        serializer = RegisterSerializer(user)
        return Response(serializer.data)
    

class update_user(GenericAPIView):
    serializer_class = RegisterSerializer

    def put(self,request,id):
        user = Registration.objects.get(pk=id)
        serializer = RegisterSerializer(instance = user, data = request.data, partial = True)

        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'message': 'User updated successfully', 'success': True}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Delete_user(GenericAPIView):
    serializer_class = RegisterSerializer


    def delete(self,request,id):
        user = Registration.objects.get(pk=id)

        user.delete()    
        return Response({'message': 'User deleted successfully', 'success': True}, status=status.HTTP_200_OK)




# PRODUCT ADD, VIEW, UPDATE, DELETE

class Add_Product(GenericAPIView):
    serializer_class = ProductSerializer

    def post(self,request):
        product_name = request.data.get('product_name')
        price = request.data.get('price')
        image = request.data.get('image')
        category = request.data.get('category')

        product_data = {
            'product_name' : product_name,
            'price' : price,
            'image' : image,
            'category' : category
        }

        serializer = ProductSerializer(data = product_data)

        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'message': 'Product added successfully', 'success': True}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class View_All_Product(GenericAPIView):
    serializer_class = ProductSerializer

    def get(self,request):
        product = Product.objects.all()

        if product.count() > 0:
            serializer = ProductSerializer(product, many = True)
            return Response({'data': serializer.data, 'message': 'All Products are given'}, status= status.HTTP_200_OK)

        return Response({'Message': 'No Data Available'}, status=status.HTTP_400_BAD_REQUEST) 
    

class View_Single_Product(GenericAPIView):
    serializer_class = ProductSerializer

    def get(self,request,id):
        product = Product.objects.get(pk=id)   
        serializer = ProductSerializer(product) 
        return Response(serializer.data)
    

class Delete_Product(GenericAPIView):
    serializer_class = ProductSerializer

    def delete(self,request,id):
        product = Product.objects.get(pk=id)

        product.delete()
        return Response({'Message': 'Product deleted successfully', 'success' :True},status=status.HTTP_200_OK)    

        
class Review_Product(GenericAPIView):
    serializer_class = ReviewSerializer

    def post(self,request):
        product_id = request.data.get('product_id')
        user_id = request.data.get('user_id')
        product_name = ""
        user_name = ""
        description = request.data.get('description')

        product_data = Product.objects.filter(id=product_id).values()

        if not product_data:
            return Response({'Message' : 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        for i in product_data:
            product_name = i.get('product_name', '')
            print(product_name)

        user_data = Registration.objects.filter(login_id = user_id).values()

        if not user_data:
            return Response({'Message' : 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        for i in user_data:
            user_name = i.get('name','')
            print(user_name)

        current_time = datetime.now().isoformat()    


        serializer = self.serializer_class(
            data = {
                'product_id' : product_id,
                'user_id' : user_id,
                'product_name' : product_name,
                'user_name' : user_name,
                'time' : current_time,
                'description' : description,
            }
        ) 

        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'Message' : 'Review added successfully'}, status=status.HTTP_200_OK)   

        return Response({'data' : serializer.errors, 'Message' : 'Failed to add review'}, status=status.HTTP_400_BAD_REQUEST)  


class View_All_Review(GenericAPIView):
    serializer_class = ReviewSerializer

    def get(self,request):
        review = ReviewProduct.objects.all()   

        if review.count() > 0:
            serializer = ReviewSerializer(review, many = True)
            return Response({'data' : serializer.data, 'message' : 'All reviews'}, status=status.HTTP_200_OK)   
        
        return Response({"Message" : 'No Reviews available'}, status=status.HTTP_400_BAD_REQUEST)
    

class View_Single_Review(GenericAPIView):
    serializer_class = ReviewSerializer

    def get(self,request,product_id):
        review = ReviewProduct.objects.get(product_id=product_id)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    

class Update_Review(GenericAPIView):
    serializer_class = ReviewSerializer

    def put(self,request,id):
        review = ReviewProduct.objects.get(pk=id)
        serializer =  ReviewSerializer(instance=review, data=request.data, partial = True) 

        if serializer.is_valid():
            serializer.save()
            return Response({'data' : serializer.data, 'message' : 'Review updated successfully', 'success' : True}, status=status.HTTP_200_OK)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class Delete_Review(GenericAPIView):
    serializer_class = ReviewSerializer

    def delete(self,request,id):
        review = ReviewProduct.objects.get(pk=id)
        review.delete()
        return Response({'message':'Review deleted successfully', 'success' : True},status=status.HTTP_200_OK)
    





# CART PAGE -- ADD, VIEW, DELETE

class Add_To_Cart(GenericAPIView):
    serializer_class = CartSerializer

    def post(self, request):
        product_id = request.data.get('product_id')
        user_id = request.data.get('user_id')
        quantity = 1
        cart_status = 1 # Default quantity is 1

        # Check if the item already exists in the cart
        cart = Cart.objects.filter(product_id=product_id, user_id=user_id)
        if cart.exists():
            return Response({'Message': 'Item already exists', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the product data
        product_data = Product.objects.filter(id=product_id).first()
        if not product_data:
            return Response({'Message': 'Product not found', 'success': False}, status=status.HTTP_404_NOT_FOUND)

        # Extract the product details
        product_name = product_data.product_name
        price = product_data.price
        image = product_data.image
        total_price = price * quantity

        # Debugging log (optional)
        print(f"Total Price: {total_price}")

        # Prepare the data to be serialized and saved
        serializer = self.serializer_class(
            data={
                'product_id': product_id,
                'user_id': user_id,
                'product_name': product_name,
                'price': price,
                'quantity': quantity,
                'image': image  # No need to get from `request.FILES`, it's from the database
            }
        )

        # Validate and save the cart item
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'Message': 'Added to cart successfully', 'success': True}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class View_All_Item_Cart(GenericAPIView):
    serializer_class = CartSerializer

    def get(self,request):
        cart = Cart.objects.all()   

        if cart.count() > 0:
            serializer = CartSerializer(cart, many = True)
            return Response({'data' : serializer.data, 'message' : 'All Cart Items'}, status=status.HTTP_200_OK)   
        
        return Response({"Message" : 'No Cart items available'}, status=status.HTTP_400_BAD_REQUEST)
    

class Delete_Cart_Item(GenericAPIView):
    serializer_class = CartSerializer

    def delete(self,request,user_id):
        cart_item = Cart.objects.get(user_id=user_id)
        cart_item.delete()
        return Response({'Message' : 'Item deleted successfully', 'success' : True}, status=status.HTTP_200_OK)
    




# WISHLIST ------ADD, VIEW, DELETE

class Add_To_Fav(GenericAPIView):
    serializer_class = WishlistSerializer  

    def post(self,request):
        product_id = request.data.get('product_id')
        user_id = request.data.get('user_id')

        wishlist = WishList.objects.filter(product_id=product_id, user_id=user_id).first()

        if wishlist:
            wishlist.delete()
            return Response({'Message': 'Item removed from favorites', 'success': True}, status=status.HTTP_200_OK)

        
        else:
            product_data = Product.objects.filter(id=product_id).first()
            # If product does not exist, return an error response
            if not product_data:
                return Response({'Message': 'Product not found', 'success': False}, status=status.HTTP_404_NOT_FOUND)

            # Extract product details
            product_name = product_data.product_name
            price = product_data.price
            image = product_data.image

            serializer = self.serializer_class(
                data = {
                    'product_id' : product_id,
                    'user_id' :user_id,
                    'product_name' : product_name,
                    'price' : price,
                    'image' : image
                }
            ) 

            if serializer.is_valid():
                serializer.save()
                return Response({'data' : serializer.data, 'Message' : 'Addede to Favorites successfully', 'success' : True}, status=status.HTTP_200_OK)

            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST) 


class View_All_Item_Fav(GenericAPIView):
    serializer_class = WishlistSerializer

    def get(self,request):
        fav = WishList.objects.all()   

        if fav.count() > 0:
            serializer = WishlistSerializer(fav, many = True)
            return Response({'data' : serializer.data, 'message' : 'All Wishlist Items'}, status=status.HTTP_200_OK)   
        
        return Response({"Message" : 'No Wishlist items available'}, status=status.HTTP_400_BAD_REQUEST)   


class Delete_Fav_Items(GenericAPIView):
    serializer_class = WishlistSerializer   

    def delete(self,request,user_id):
        fav_item = WishList.objects.get(user_id = user_id)
        fav_item.delete()
        return Response({'Message' : 'Item deleted successfully', 'success' : True}, status=status.HTTP_200_OK)          




# ADDRESS - ADD, VIEW, UPDATE, DELETE

class Add_Address(GenericAPIView):
    serializer_class = AddressSerializer

    def post(self, request):
        user_id = request.data.get('user_id') 
        name = request.data.get('name')
        number = request.data.get('number')
        address = request.data.get('address')
        pincode = request.data.get('pincode')
        locality = request.data.get('locality')
        city = request.data.get('city')
        state = request.data.get('state')

        serializer = self.serializer_class(
            data={
                'user_id': user_id,  # Correct 'user_id'
                'name': name,
                'number': number,             
                'address': address,
                'pincode': pincode,
                'locality': locality,
                'city': city,
                'state': state
            }
        )

        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'Message': 'Address added successfully', 'success': True}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class View_Address(GenericAPIView):
    serializer_class = AddressSerializer

    def get(self,request):
        address = Address.objects.all()

        if address.count() > 0:
            serializer = AddressSerializer(address, many = True)
            return Response({'data' : serializer.data, 'Message' : 'Addresses', 'success' : True}, status=status.HTTP_200_OK)
        
        return Response({ 'Message' : 'No address found'}, status=status.HTTP_400_BAD_REQUEST)
    

class Update_Address(GenericAPIView):
    serializer_class = AddressSerializer

    def put(self,request,user_id):
        address = Address.objects.get(user_id=user_id)

        serializer = AddressSerializer(instance = address, data = request.data, partial = True) 

        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data, 'Message' : 'Address Updated Successfully'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    

class Delete_Address(GenericAPIView):
    serializer_class = AddressSerializer

    def delete(self,request,user_id):
        address = Address.objects.get(user_id=user_id)
        address.delete()
        return Response({'Message' : 'Deleted Address Successfully', 'success' : True}, status=status.HTTP_200_OK)

       
       
       

# ORDER - PLACE ORDER, VIEW



class Place_Order(GenericAPIView):
    serializer_class = OrderSerializer

    def post(self, request, user_id):
        cart_items = Cart.objects.filter(user_id=user_id, cart_status=1)

        if cart_items.exists():
            orders = []

            for item in cart_items:
                order_data = {
                    'product_id': item.product_id,
                    'user_id': item.user_id,
                    'product_name': item.product_name,
                    'quantity': item.quantity,
                    'price': item.price,
                    'image': item.image
                }

                serializer = self.serializer_class(data=order_data)

                if serializer.is_valid():
                    serializer.save()
                    orders.append(serializer.data)
            cart_items.delete()

            return Response({'Message': 'Order(s) placed successfully', 'orders': orders}, status=status.HTTP_200_OK)

        else:
            return Response({'Message': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)


class View_Orders(GenericAPIView):
    serializer_class = OrderSerializer

    def get(self,request):
        orders = Order.objects.all()
        
        if orders.count() > 0:
            serializer = OrderSerializer(orders, many = True)
            return Response({'data' : serializer.data, 'Message' : 'Orders', 'success' :True}, status=status.HTTP_200_OK)
        
        return Response({'Message' : 'No Orders found'}, status=status.HTTP_400_BAD_REQUEST)
    

class View_Single_Order(GenericAPIView):
    serializer_class = OrderSerializer

    def get(self,request,user_id):
        order = Order.objects.filter(user_id=user_id)
        serializer = OrderSerializer(order,many=True)
        return Response(serializer.data)    
    



# SEARCH

class Search_Item(GenericAPIView):
    serializer_class = ProductSerializer

    def post(self, request):

        search_query = request.data.get('search_query', '')

        if search_query:
            # Filter products based on the search query
            products = Product.objects.filter(
                Q(product_name__icontains=search_query) | Q(category__icontains=search_query)
            )
            print("Filtered Products:", products)  # Debugging output to see filtered results

            # If no products are found
            if not products:
                return Response({'Message': 'No products found'}, status=status.HTTP_404_NOT_FOUND)

            # Serialize the filtered products
            serializer = self.serializer_class(products, many=True)

            # Add full image URL if image exists
            for product in serializer.data:
                if product['image']:
                    product['image'] = settings.MEDIA_URL + product['image']

            return Response({'data': serializer.data, 'Message': 'Image fetched successfully'}, status=status.HTTP_200_OK)

        return Response({'Message': 'No query found'}, status=status.HTTP_400_BAD_REQUEST)
    


# PASSWORD

class Change_Password(GenericAPIView):
    serializer_class = LoginSerializer

    def put(self, request, id):
        try:
            user = Login.objects.get(pk=id)  # Get user by ID
        except Login.DoesNotExist:
            return Response({'Message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(user, data=request.data, partial=True)

        if serializer.is_valid():
            new_password = serializer.validated_data.get('password')
            if new_password:
                user.password = new_password  # Directly set the new password
                user.save()  # Save the updated user object
                return Response({'Message': 'Password updated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'Message': 'No password provided'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'Message': 'Password update failed', 'Errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)