from django.urls import path
from . import views

urlpatterns = [   
	path('', views.home, name="home"),
    path('store/', views.store, name="store"),
    path('store/<slug:category_slug>/', views.store, name='products_by_category'),
    path('store/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    
	path('cart/', views.cart, name="cart"),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/', views.remove_cart, name= 'remove_cart'),
    path('remove_cart_item/<int:product_id>/', views.remove_cart_item, name= 'remove_cart_item'),

	path('checkout/', views.checkout, name="checkout"),
	path('update_item/', views.update_item, name="update_item"),
    path('process_order/', views.processOrder, name="process_order")

]