
from django.shortcuts import render
from django.http import JsonResponse, HttpRequest
from .models import *
import json
# Create your views here.


def store(request):
    """
    This view renders the main store page along with all
    the products for sale. Users can add items to their cart in
    this view
    """
    products = Product.objects.all
    context = {'products': products}
    return render(request, 'store/store.html', context)


def cart(request):
    """
    This view renders the cart items in current order
    along with the total prices
    """
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        items = []
    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)


def checkout(request):
    """
    This view renders the checkout page along with
    forms to add payment and shipping info
    """
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        items = []
    context = {'items': items, 'order': order}
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
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()            

    return JsonResponse('Item added', safe = False)
