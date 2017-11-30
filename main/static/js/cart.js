const getCookie = (name = '') => {
    if (!document.cookie || document.cookie === '') return null
    return document.cookie.split(';').find(c => c.split("=")[0] === name)
}

const csrftoken = getCookie('csrftoken')

const onChangeAmount = (event = window.event) => {

    const form = event.target.parentNode.parentNode
    const headers = new Headers({'Cookie': csrftoken})
    // const headers = new Headers()
    const body = new FormData(form)
    const init = {method: 'POST', headers, body, credentials: 'include'}
    fetch('/update-order/', init)
        .then(response => response.json())
        .then(updateInfo)
        .catch(console.error)
}

const fetchInfo = async (csrftoken, formData, method = 'POST', url) => {
    const headers = new Headers({'Cookie': csrftoken})
    const body = new FormData(formData)
    body.forEach(console.log)
    const init = {method, headers, body, credentials: 'include'}
    try {
        const response = await fetch(url, init)
        return await response.json()
    } catch (err) {
        console.error(err)
        return err
    }
}

const onChangeShipping = async (event = window.event) => {
    const form = event.target.parentNode.parentNode
    const {grandTotalPrice, shipping} = await fetchInfo(csrftoken, form, 'POST', '/change-shipping/')
    document.getElementById('select-shipping').value = shipping
    document.getElementById('grand-total-price').innerText = grandTotalPrice
}

const updateInfo = ({amount, productId, totalPrice, subTotalPrice, grandTotalPrice}) => {
    document.getElementById(`product-amount-${productId}`).value = amount
    document.getElementById(`product-total-price-${productId}`).innerText = totalPrice
    document.getElementById('sub-total-price').innerText = subTotalPrice
    document.getElementById('grand-total-price').innerText = grandTotalPrice
}

const onRemoveOrder = async (event = window.event) => {
    const form = event.target.parentNode.parentNode
    const {orders} = await fetchInfo(csrftoken, form, 'POST', '/remove-product-ajax/')
}

const amountElements = document.getElementsByName('amount')
amountElements.forEach(element => element.addEventListener('change', onChangeAmount))

document.getElementById('select-shipping').addEventListener('change', onChangeShipping)

document.getElementsByName('product-remove').forEach(element => element.addEventListener('click', onRemoveOrder))