from django.shortcuts import render
from .models import Product
from django.http import HttpResponse

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

    



