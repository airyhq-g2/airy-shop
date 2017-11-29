const basketToggler = document.getElementById('basket-toggler')
const hamburgerToggler = document.getElementById('hamburger-toggler')
const basketMenu = document.getElementById('basket-menu')
const hamburgerMenu = document.getElementById('hamburger-menu')

const elements = {
    'basket-toggler': {
        toggler: basketToggler,
        menu: basketMenu
    },
    'hamburger-toggler': {
        toggler: hamburgerToggler,
        menu: hamburgerMenu
    }
}

let currentExpandedMenu = ''

const collapseMenuListener = (event = window.event) => {
    const elementKeys = Object.keys(elements)
    if (elements.hasOwnProperty(event.target.id)) {
        shouldExpandOrCollapseMenu(elementKeys, event.target.id)
    } else {
        collapseAllMenu(elementKeys)
    }
}

const shouldExpandOrCollapseMenu = (elementKey = [], targetId = '') => {
    elementKey.forEach(
        (key) => {
            if (key === targetId && currentExpandedMenu !== targetId) {
                expandMenu(elements[key].menu, key)
            } else {
                collapseMenu(elements[key].menu, key)
            }
        })

}

const expandMenu = (menu, key = '') => {
    menu.style.maxHeight = '100%'
    currentExpandedMenu = key
}

const collapseMenu = (menu, key = '') => {
    menu.style.maxHeight = '0%'
    currentExpandedMenu = currentExpandedMenu === key ? '' : currentExpandedMenu
}

const collapseAllMenu = (elementKeys = []) => elementKeys.forEach(key => collapseMenu(elements[key].menu, key))


document.addEventListener('click', collapseMenuListener)
