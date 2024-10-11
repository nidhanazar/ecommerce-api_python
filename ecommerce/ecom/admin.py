from django.contrib import admin

from . models import Registration,Login,Product,ReviewProduct,Cart,WishList, Address

# Register your models here.
admin.site.register(Registration)
admin.site.register(Login)
admin.site.register(Product)
admin.site.register(ReviewProduct)
admin.site.register(Cart)
admin.site.register(WishList)
admin.site.register(Address)
