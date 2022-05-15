import imp
import json
from .models import *

def cartData(request):
    """
    Returns an dictionary outlining a cart: cartItems, items, and order; using
    'cart' cookie from current request. Loads order from a cookie or database
    depending on whether a user is logged in or a guest is shopping
    """
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_total_items
    else:
        cookieData = cookieCart(request)
        items = cookieData['items']
        order = cookieData['order']
        cartItems = cookieData['cartItems']
    return {'items': items, 'order': order, 'cartItems': cartItems}

def cookieCart(request):
    """
    Returns an dictionary outlining a cart(from guest cookie): cartItems, items, and order; using
    'cart' cookie from current request
    """

    #load the cart cookie as a dictionary object
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    order = {'get_cart_total': 0, 'get_total_items': 0, 'shipping': False}
    cartItems = order['get_total_items']
    items = []

    #iterate through the cart json object using where i is a key representing
    #a product id
    for i in cart:
        try:
                
            #Calculate total cart items from the quantities in the cart cookie
            cartItems += cart[i]['quantity']

            #get the product from database using the i key as the product id 
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_total_items'] += cart[i]['quantity']

            # create an item object from the parameters sent in request
            # to fill current guest cart object
            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price':product.price,
                    'imageURL':product.imageURL
                },
                'quantity': cart[i]['quantity'],
                'get_total': total
            }

            #add current item to the items object used in view context
            items.append(item)

            #set order to shipping if product is not digital
            if product.digital == False:
                order['shipping'] = True
        except:
            pass
    return {'cartItems': cartItems, 'order': order, 'items': items}