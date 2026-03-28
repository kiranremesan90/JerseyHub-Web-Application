from django.shortcuts import render
from .models import Product
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def about(request):
    return render(request,'about.html')

def checkout(request):
    return render(request,'checkout.html')

def contact(request):
    return render(request,'contact.html')

def index(request):
    return render(request,'index.html')



def product(request):
    products = Product.objects.all()
    return render(request,'product.html',{'products':products})





def shoppingcart(request):
    return render(request,'shoping-cart.html')


from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib import messages

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password') 

        if password != confirm_password:
            messages.error(request,"password does not match")
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request,"username already exist")
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request,"email already exist")
            return redirect('register')
        
        # User.objects.create_user(username=username,email=email,password=password)
        # messages.success(request,"Account created successfully")

        # CREATE USER
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.save()

        messages.success(request,"Account created succesfully")
        return redirect('login')
    
    return render(request,'register.html')

from django.contrib.auth import authenticate,login


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            messages.error(request,"Invalid username or password")
            return redirect('login')
    return render(request,'login.html')

from django.shortcuts import render, get_object_or_404

def product_detail(request, id):
    product=get_object_or_404(Product, id=id)
    return render(request, 'product-detail.html', {'product': product})

from django.shortcuts import render,redirect,get_object_or_404
from .models import Product,Cart,CartItem
@login_required(login_url='login')

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        item.quantity += 1

    item.save()
    return redirect('cart')

@login_required(login_url='login')
def update_cart_item(request, item_id):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    if request.method == "POST":
        qty = int(request.POST.get('quantity', 1))

        if qty > 0:
            item.quantity = qty
            item.save()
        else:
            item.delete()

    return redirect('cart')

@login_required(login_url='login')
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    return render(request, 'shoping-cart.html', {
        'cart': cart,
        'cart_items': cart_items
    })


@login_required(login_url='login')
def remove_item(request, id):
    item = get_object_or_404(CartItem, id=id)
    item.delete()
    return redirect('cart')

from django.contrib.auth import logout
from django.shortcuts import redirect

# checkout

import razorpay
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Cart, CartItem, Orderr, OrderItemm

@login_required(login_url='login')
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        return redirect('cart')

    total = sum(item.product.price * item.quantity for item in cart_items)
    delivery_charge = 50
    grand_total = total + delivery_charge

    if request.method == "POST":
        # 1️⃣ Create order
        order = Orderr.objects.create(
            user=request.user,
            full_name=request.POST.get('full_name'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            pincode=request.POST.get('pincode'),
            total_amount=grand_total
        )

        # 2️⃣ Copy cart items into OrderItems
        for item in cart_items:
            OrderItemm.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # 3️⃣ Clear cart immediately
        cart_items.delete()

        # 4️⃣ Create Razorpay order
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )
        payment = client.order.create({
            "amount": int(grand_total * 100),
            "currency": "INR",
            "payment_capture": 1
        })
        order.razorpay_order_id = payment['id']
        order.save()

        # 5️⃣ Render payment page
        return render(request, 'payment.html', {
            'order': order,
            'order_items': order.orderitemm_set.all(),
            'razorpay_key': settings.RAZORPAY_KEY_ID,
            'amount': int(grand_total * 100)
        })

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'delivery_charge': delivery_charge
    })

@csrf_exempt
@login_required(login_url='login')
def payment_success(request):
    if request.method == "POST":
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        order = get_object_or_404(Orderr, razorpay_order_id=razorpay_order_id)

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })

            order.is_paid = True
            order.razorpay_payment_id = razorpay_payment_id
            order.save()

            return redirect('order_success')

        except:
            return redirect('payment_failed')


@login_required(login_url='login')
def payment_page(request, order_id):
    order = get_object_or_404(Orderr, id=order_id)

    return render(request, 'payment.html', {
        'order': order,
        'razorpay_key': settings.RAZORPAY_KEY_ID,
        'amount': int(order.total_amount * 100)  # amount in paise
    })


@login_required(login_url='login')
def order_success(request):
    order = Orderr.objects.filter(user=request.user, is_paid=True).last()
    return render(request, 'success.html', {'order': order})


def payment_failed(request):
    return render(request, 'failed.html', {'message': "Your payment was not completed."})


def user_logout(request):
    logout(request)
    return redirect('login')  # or 'index'

