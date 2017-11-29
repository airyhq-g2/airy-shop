const getCookie = (name = '') => {
    if (!document.cookie || document.cookie === '') return null
    return document.cookie.split(';').find(c => c.split("=")[0] === name)
}

const onChangeAmount = (event = window.event) => {
    const csrftoken = getCookie('csrftoken')
    const form = event.target.parentNode.parentNode
    const headers = new Headers({'Cookie': csrftoken})
    const body = new FormData(form)
    const init = {method: 'POST', headers, body, credentials: 'include'}
    fetch('/update-order/', init)
        .then(response => response.json())
        .then(updateInfo)
        .catch(console.error)
}

const updateInfo = ({amount, productId, totalPrice, subTotalPrice, grandTotalPrice}) => {
    document.getElementById(`product-amount-${productId}`).value = amount
    document.getElementById(`product-total-price-${productId}`).innerText = totalPrice
    document.getElementById('sub-total-price').innerText = subTotalPrice
    document.getElementById('grand-total-price').innerText = grandTotalPrice
}

const amountElements = document.getElementsByName('amount')
amountElements.forEach(element => element.addEventListener('change', onChangeAmount))