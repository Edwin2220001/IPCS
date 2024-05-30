from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpRequest, HttpResponse, request, JsonResponse
import json
from .models import *



def home(request, quantity= 0, cart_items= None):
    categories= Category.objects.all()
    products= Product.objects.all()

    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_items= CartItem.objects.filter(cart= cart, is_active= True)
    for cart_item in cart_items:
        quantity+= cart_item.quantity
        
    context= {'categories': categories, 'products':products, 'quantity': quantity}
    return render(request, 'home.html', context)

    
def store(request, category_slug= None, quantity= 0, cart_items= None):
    cates= None
    products= None
    categories= Category.objects.all()
    
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_items= CartItem.objects.filter(cart= cart, is_active= True)
    for cart_item in cart_items:
        quantity+= cart_item.quantity 

    if category_slug:
        cates= get_object_or_404(Category, slug= category_slug)
        products= Product.objects.filter(category= cates, is_available= True)
    else:
        products= Product.objects.filter(is_available= True)

    context= {'categories': categories, 'products': products, 'quantity': quantity}    
    return render(request, 'store/store.html', context)



def product_detail(request, category_slug, product_slug, quantity= 0, cart_items= None):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_items= CartItem.objects.filter(cart= cart, is_active= True)
    for cart_item in cart_items:
        quantity+= cart_item.quantity
        
    print(f"category_slug: {category_slug}, product_slug: {product_slug}")
    try:
        single_product= Product.objects.get(category__slug= category_slug, slug= product_slug)
    except Exception as e:
        raise e    
    
    context= { 'single_product': single_product, 'quantity': quantity}
    return render(request, 'store/product_detail.html', context)


def _cart_id(request):
    cart= request.session.session_key
    if not cart:
        cart= request.session.create()
    return cart

def add_cart(request, product_id):
    product= Product.objects.get(id= product_id)
    print("Product ID:", product.id)
    try:
        cart= Cart.objects.get(cart_id= _cart_id(request))
    except Cart.DoesNotExist:
        cart= Cart.objects.create(cart_id= _cart_id(request))    
    cart.save()    

    try:
        cart_item= CartItem.objects.get(product= product, cart= cart)
        cart_item.quantity+= 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item= CartItem.objects.create(
            product= product,
            quantity= 1,
            cart= cart
        )
        cart_item.save()
    return redirect('cart')

def remove_cart(request, product_id):
    cart= Cart.objects.get(cart_id= _cart_id(request))
    product= get_object_or_404(Product, id= product_id)
    cart_item= CartItem.objects.get(product= product, cart= cart)

    if cart_item.quantity > 1:
        cart_item.quantity-= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def remove_cart_item(request, product_id):
    cart= Cart.objects.get(cart_id= _cart_id(request))
    product= get_object_or_404(Product, id= product_id)
    cart_item= CartItem.objects.get(product= product, cart= cart)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items= None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    cart_items= CartItem.objects.filter(cart= cart, is_active= True)
    
    for cart_item in cart_items:
        total+= (cart_item.product.price * cart_item.quantity)
        quantity+= cart_item.quantity  

    tax= (2*total)/100
    grand_total= total+ tax 

    context= {'total': total, 'quantity': quantity, 'cart_items': cart_items, 'tax': tax, 'grand_total': grand_total}
    return render(request, 'store/cart.html', context)



def checkout(request, total=0, quantity= 0, grand_total= 0, cart_items= None):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_items= CartItem.objects.filter(cart= cart, is_active= True)
    for cart_item in cart_items:
        total+= (cart_item.product.price * cart_item.quantity)
        quantity+= cart_item.quantity

    tax= (2*total)/100
    grand_total= total+ tax
    context= {'cart_items': cart_items, 'quantity': quantity, 'grand_total': grand_total}

    return render(request, 'store/checkout.html', context)
