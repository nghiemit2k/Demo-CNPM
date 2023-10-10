function addToCart(id,name,price) {
    event.preventDefault()

    fetch('/api/add-to-cart', {
        method: 'post',
        body: JSON.stringify({
            'id':id,
            'name': name,
            'price': price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function (res) {
        return res.json()
    }).then(function (data) {
          let d = document.getElementById('cartCounter')
        d.innerText = data.total_quantity
    })
}

function pay() {
    if(confirm('Ban chac chan thanh toan ko?') === true) {
       fetch('/api/pay', {
           method:'post'
       }).then(function (res) {
           return res.json()
       }).then(function (data) {
           if(data.code ===200)
               location.reload()
       })
    }
}
