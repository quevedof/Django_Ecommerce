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


# view for login.html
def loginPage(request):
    # ensure users that are logged in cannot access the login page
    if request.user.is_authenticated:
        return redirect('store')
    else:
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
def signup(request):
    # ensure users that are logged in cannot access the sign up page
    if request.user.is_authenticated:
        return redirect('store')
    else:
        # if data is submitted, create a new user form
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            # validate data
            if form.is_valid():
                new_user = form.save()

                Customer.objects.create(user=new_user, name=new_user.first_name, email=new_user.email)
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

    return JsonResponse('Payment complete', safe=False)


