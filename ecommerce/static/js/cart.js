var updateBtns = document.getElementsByClassName('update-cart')

for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'action: ', action)

        console.log('USER: ', user)
        if (user === 'AnonymousUser') {
            addCookieItem(productId, action)
        } else {
            updateUserOrder(productId, action)
        }
    });
}

/**Returns passed 'obj' without the the key 'property' */
function withoutProperty(obj, property) {  
    const { [property]: unused, ...rest } = obj

  return rest
}

/** Makes a guest cart for anonymous user by making a cookie that holds relevant cart information*/
function addCookieItem(productId, action) {
    // console.log('Not logged in')

    //Cart object used here is created in header file of base.html

    if (action == 'add') {
        if (cart[productId] == undefined) {
            cart[productId] = {'quantity': 1}
        }
        else {
            cart[productId]['quantity' ] += 1
        }
    }
    if (action == 'subtract') {
        console.log('Subtract item')
        cart[productId]['quantity'] -= 1

        if (cart[productId]['quantity'] <= 0) {
            // delete cart[productId]
            console.log('poop')
            subtractCart = withoutProperty(cart, productId)
            cart = subtractCart  
        }
    }

    //Overwrite cart cookie
    console.log('Cart:' , cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}

/**   Sends productId and action as a JSON object to 
 * the 'update_item' view to update user order */
function updateUserOrder(productId, action) {
    console.log('User is logged in, sending data...')

    var url = '/update_item/'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'productId': productId, 'action': action })
    })

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            console.log('data: ', data)
            location.reload()

        })
}