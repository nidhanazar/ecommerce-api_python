
from django.urls import path,include

from . import views

urlpatterns = [
    path('',views.index),
    path('register/', views.Register_view.as_view()),
    path('login/',views.Login_view.as_view()),
    path('all_users/',views.All_users_view.as_view()),
    path('single_user_view/<int:id>',views.Single_user_view.as_view()),
    path('update_user/<int:id>',views.update_user.as_view()),
    path('delete/<int:id>',views.Delete_user.as_view()),
    path('add_product/',views.Add_Product.as_view()),
    path('view_all_product/',views.View_All_Product.as_view()),
    path('view_single_product/<int:id>/',views.View_Single_Product.as_view()),
    path('delete_product/<int:id>/',views.Delete_Product.as_view()),
    path('review_product/',views.Review_Product.as_view()),
    path('view_all_review/',views.View_All_Review.as_view()),
    path('view_single_review/<int:product_id>',views.View_Single_Review.as_view()),
    path('update_review/<int:id>/',views.Update_Review.as_view()),
    path('delete_review/<int:id>',views.Delete_Review.as_view()),
    path('add_to_cart/',views.Add_To_Cart.as_view()),
    path('view_all_item_cart',views.View_All_Item_Cart.as_view()),
    path('delete_cart_item/<int:user_id>',views.Delete_Cart_Item.as_view()),
    path('add_to_fav/',views.Add_To_Fav.as_view()),
    path('view_all_item_fav/',views.View_All_Item_Fav.as_view()),
    path('delete_fav_items/<int:user_id>/',views.Delete_Fav_Items.as_view()),
    path('add_address/',views.Add_Address.as_view()),
    path('view_address/',views.View_Address.as_view()),
    path('update_address/<int:user_id>',views.Update_Address.as_view()),
    path('delete_address/<int:user_id>',views.Delete_Address.as_view()),
    path('place_order/<int:user_id>/', views.Place_Order.as_view()),
    path('view_orders/',views.View_Orders.as_view(),),
    path('view_single_order/<int:user_id>',views.View_Single_Order.as_view()),
    path('search_item/',views.Search_Item.as_view()),
    path('change_password/<int:id>/',views.Change_Password.as_view()),
]