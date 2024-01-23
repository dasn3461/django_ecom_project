from django.shortcuts import render,redirect
from .models import Category,Product,Cart
from django.contrib import messages
from .forms import CustomUserForm
from django.contrib.auth import authenticate,login,logout
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# Create your views here.
def home(request):
    products=Product.objects.filter(trending=1)
    return render(request, 'shop/index.html', {'products':products})


def register(request):
    form=CustomUserForm()
    if request.method=="POST":
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Registration success you can login now!')
            return redirect('/login')
    return render(request, 'shop/register.html', {'form':form})



def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method=="POST":
            unm=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request, username=unm,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request, "Logged in Successfully!!")
                return redirect("/")
            else:
                messages.error(request, 'Invalid username and Password!!')
                return redirect('/login')
        return render(request, 'shop/login.html')


def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Loggedout Successfully !!')
    return redirect("/")
        

def collections(request):
    category=Category.objects.filter(status=0)
    return render(request, 'shop/collections.html', {'category':category})



def collections_view(request,name):
    if(Category.objects.filter(name=name,status=0)):
        products=Product.objects.filter(category__name=name)
        return render(request, 'shop/products/index.html', {'products':products, 'category_name':name})
    
    else:
        messages.warning(request,'No Such Category Found')
        return redirect('collections')
    
    
    
def product_details(request,cname,pname):
    if(Category.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
            products=Product.objects.filter(name=pname,status=0).first()
            return render(request, 'shop/products/product_details.html', {'products':products})
        
        else:
            messages.error(request,'No Such Product Found')
            return redirect('collections')    
        
    else:
        messages.error(request,'No Such Category Found')
        return redirect('collections')     
    
    







def add_to_cart(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            try:
                data = json.loads(request.body.decode('utf-8'))
                product_qty = data['product_qty']
                product_id = data['pid']
                product_status = get_object_or_404(Product, id=product_id)
                if Cart.objects.filter(user=request.user.id, product_id=product_id).exists():
                    return JsonResponse({'status': 'Product already in cart'}, status=200)

                if product_status.quantity >= product_qty:
                    Cart.objects.create(user=request.user, product_id=product_id, product_qty=product_qty)
                    return JsonResponse({'status': 'Product added to cart'}, status=200)
                else:
                    return JsonResponse({'status': 'Product stock not available'}, status=200)

            except json.JSONDecodeError:
                return JsonResponse({'status': 'Invalid JSON data'}, status=400)

        else:
            return JsonResponse({'status': 'Login to add to cart'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=200)
    


def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request, 'shop/cart.html', {'cart':cart})
    else:
        return redirect("/")    
    
def remove_cart_page(request, cid):
    cartitem = Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect("cart")
