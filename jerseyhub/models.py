from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name=models.CharField(max_length=255)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    description=models.TextField()
    image=models.ImageField(upload_to='products/')
    category=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
# class Cart(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)

# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product,on_delete=models.CASCADE)
#     quantity = models.PositiveBigIntegerField(default=+1)

#     def total_price(self):
#         return self.product * self.quantity



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def total_price(self):
        return sum(item.total_price() for item in self.cartitem_set.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity
    


from django.db import models
from django.contrib.auth.models import User
    

class Orderr(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

# payment

    total_amount = models.DecimalField(max_digits=10,decimal_places=2)
    is_paid = models.BooleanField(default=False)

# Razorpay Ids

    razorpay_order_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=200,blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Order {self.id}"


class OrderItemm(models.Model):
    order = models.ForeignKey(Orderr, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10,decimal_places=2)

    @property
    def total_price(self):
        return self.price * self.quantity



