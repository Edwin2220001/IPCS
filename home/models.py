from django.db import models
from django.utils import timezone as tz
from django.urls import reverse


class Category(models.Model):
    name= models.CharField(max_length=225, unique=True)
    slug= models.SlugField(max_length=225, unique=True)
    description= models.TextField(default="")
    img= models.ImageField()

    def __str__(self):
        return self.name
    
    def get_url(self):
        return reverse('products_by_category', args= [self.slug])


class Product(models.Model):
    name= models.CharField(max_length= 100, null=True)
    category= models.ForeignKey(Category, on_delete=models.CASCADE)
    price= models.DecimalField(max_digits= 10, decimal_places= 2)
    digital= models.BooleanField(default=False, null=True, blank=False)
    image= models.ImageField(null=True, blank=True)
    slug= models.SlugField(max_length=70, unique=True)
    desc= models.TextField(max_length=255, blank=True)
    stock= models.IntegerField(default=0)
    is_available= models.BooleanField(default= True)
    created_date= models.DateTimeField(default= tz.now)
    modified_date= models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.name    

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    @property
    def imageURL(self):
        try:
            url= self.image.url
        except:
            url= ''
        return url        
    
    

class Cart(models.Model):
    cart_id = models.CharField(max_length=225, blank=True)
    date_added = models.DateField(auto_now_add= True)

    def __str__(self):
        return self.cart_id 
    

class CartItem(models.Model):
    product= models.ForeignKey(Product, on_delete= models.CASCADE)
    cart= models.ForeignKey(Cart, on_delete= models.CASCADE) 
    quantity= models.IntegerField()
    is_active= models.BooleanField(default= True)

    def __str__(self):
        return self.product
    
    
    def sub_total(self):
        return self.product.price * self.quantity



class ShippingAddress(models.Model):
    address= models.CharField(max_length= 150, null= True)
    city= models.CharField(max_length= 150, null= True)
    state= models.CharField(max_length= 150, null= True)
    zipcode= models.CharField(max_length= 150, null= True)
    date_added= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    
    

class Order(models.Model):
    date_ordered= models.DateTimeField(auto_now_add= True)
    complete= models.BooleanField(default= False)
    transaction_id= models.CharField(max_length=100, null= True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping= False
        orderitems= self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping= True
        return shipping

    @property
    def get_cart_total(self):
        orderitems= self.orderitem_set.all()
        total= sum([item.get_total for item in orderitems])
        return total 

    @property    
    def get_cart_items(self):
        orderitems= self.orderitem_set.all()
        total= sum([item.quantity for item in orderitems])
        return total



class OrderItem(models.Model):
    product= models.ForeignKey(Product, on_delete=models.SET_NULL, null= True)
    order= models.ForeignKey(Order, on_delete=models.SET_NULL, null= True)
    quantity= models.IntegerField(default=0, null= True, blank= True)
    date_added= models.DateTimeField(auto_now_add=True)
    is_active= models.BooleanField(default= True)

    def __str__(self):
        return self.product.name  

    @property
    def get_total(self):
        total= self.product.price* self.quantity
        return total