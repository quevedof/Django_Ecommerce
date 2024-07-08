import json
from .models import *

# gets data from cookies if user is not logged in
def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

        print('Cart:', cart)
    items = []
    #template needs an order for guests
    order = {
        'get_cart_total': 0,
        'get_cart_items': 0,
        'shipping': False,
    }
    cartItems = order['get_cart_items']

    for i in cart:
        #prevent  errors if the product doesnt exist in the db
        try:
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL,
                },
                'quantity': cart[i]['quantity'],
                'get_total': total,
            }
            items.append(item)

            if product.digital == False:
                order['shipping'] = True
        except:
            pass
    return {'cartItems': cartItems, 'order': order, 'items': items}

# returns cart data from db if the user is logged in
# else, uses cookies for cart data for guest users
def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        #get if exists, or create
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        #query all orderitems that has order as a parent
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return {'cartItems': cartItems, 'order': order, 'items': items}

# order creation for guest users
def guestOrder(request, data):
    print('User is not logged in')

    print('Cookie:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(
        email = email,
    )
    customer.name = name
    customer.save()

    #create order
    order = Order.objects.create(
        customer = customer,
        complete = False
    )
    
    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderItem = OrderItem.objects.create(
            product = product,
            order = order,
            quantity = item['quantity']
        )

    return customer, order
