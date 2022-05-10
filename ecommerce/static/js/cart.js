var updateBtns = document.getElementsByClassName('update-cart')

for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'action: ', action)

        console.log('USER: ', user)
        if (user === 'AnonymousUser') {
            addCookieItem()
        } else {
            updateUserOrder(productId, action)
        }
    });
}

/** */
function addCookieItem(productId, action) {
    console.log('Not logged in')

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