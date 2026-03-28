from django.urls import path
from.import views

urlpatterns=[
    path('about/',views.about,name='about'),
    path('checkout/',views.checkout,name='checkout'),
    path('contact/',views.contact,name='contact'),
    path('',views.index,name='index'),
    path('login/',views.user_login,name='login'),
    path('product/',views.product,name='product'),
    
    path('register/',views.register,name='register'),
    path('product/<int:id>/',views.product_detail,name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart,name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('remove/<int:id>/',views.remove_item, name='remove_item'),
    path('update-item/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
     path('order_success/', views.order_success, name='order_success'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('failed/', views.payment_failed, name='payment_failed'),
        path('payment/<int:order_id>/', views.payment_page, name='payment_page'),
        path('logout/', views.user_logout, name='logout'),




    


]