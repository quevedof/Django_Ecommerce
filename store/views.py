from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cartData, guestOrder
from .forms import CreateUserForm
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .decorators import *


#ensure users that are logged in cannot access the login page by calling a decorator
@unauthenticated_user
def loginPage(request):    
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        # use the email given to get the username and login
        # allows the login of user using their email
        username = User.objects.get(email=email.lower()).username
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.info(request, 'Username OR password is incorrect.')


    context = {}
    return render(request,'store/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

# view for signup.html
@unauthenticated_user
def signup(request):
    # if data is submitted, create a new user form
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        # validate data
        if form.is_valid():
            new_user = form.save()

            Customer.objects.create(user=new_user, name=f"{new_user.first_name} {new_user.last_name}", email=new_user.email)
            # send a confirmation message to the template
            messages.success(request, 'Account successfully created, please login.')
            return redirect('login')
    else:
        form = CreateUserForm()

    context = {'form': form}
    return render(request,'store/signup.html', context)

# view for store.html
def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
   
   # show all products
    products = Product.objects.all()
    context = {
        'products': products,
        'cartItems':cartItems,
        'shipping': False,
    }
    return render(request, 'store/store.html', context)

# view for cart.html
def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {
        'items': items,
        'order': order,
        'cartItems':cartItems
    }
    return render(request, 'store/cart.html', context)

# view for checkout.html
def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {
        'items': items,
        'order': order,
        'cartItems':cartItems
    }
    return render(request, 'store/checkout.html', context)

# updates the item count on the cart.html
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1 )
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1 )

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

# processes the order as a logged in user or as a guest
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    # check if total value from the frontend == backend, to prevent frontend editing
    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        )

    return JsonResponse(order.id, safe=False)

# order confirmation view that takes the order_id as a param
def order_confirmation(request, order_id):

    order = Order.objects.get(id=order_id)

    #shipping address
    shipping_address = ShippingAddress.objects.get(customer=order.customer, order=order)
    # order items
    order_items = OrderItem.objects.filter(order=order)

    context = {
        "order": order,
        "shipping_address": shipping_address,
        "order_items": order_items
    }
    return render(request,'store/order_confirmation.html/', context)
# only admins can view the product management page
@admin_required
def products_management(request):
    context={}
    return render(request, 'store/products_management.html', context)
