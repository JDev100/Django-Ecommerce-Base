
from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse, HttpRequest
from .models import *
import json
import datetime
from .utils import cartData

# Create your views here.


def store(request):
    """
    This view renders the main store page along with all
    the products for sale. Users can add items to their cart in
    this view
    """
    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):
    """
    This view renders the cart items in current order
    along with the total prices
    """
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    context = {'items': items, 'order': order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    """
    This view renders the checkout page along with
    forms to add payment and shipping info
    """

    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)



def updateItem(request):
    """
    This view updates the user order by accessing a json object
    sent by request to Add or Subtract item from cart using productId
    to access proper product from database
    """
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action: ', action)
    print('Product: ', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order,product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'subtract':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()            

    return JsonResponse('Item added', safe = False)
def processOrder(request):
    """
    This view will process the current order in cart
    made by logged in user or anonymous user
    """
    print('Data:', request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer = customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                zipcode=data['shipping']['zipcode'],
            )

    else: 
        print('User is not logged in...')        
    return JsonResponse('Payment Complete', safe = False)
