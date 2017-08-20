const basketToggler = document.getElementById('basket-toggler')
const hamburgerToggler = document.getElementById('hamburger-toggler')
const basketMenu = document.getElementById('basket-menu')
const hamburgerMenu = document.getElementById('hamburger-menu')

const elements = [
  {
    toggler: basketToggler,
    menu: basketMenu
  },
  {
    toggler: hamburgerToggler,
    menu: hamburgerMenu
  }
]

const toggleCollapseMenu = e => {
  const togglerId = e.target.parentElement.id
  elements.forEach(element => {
    if (element.toggler.id === togglerId) {
      element.menu.style.maxHeight = element.menu.style.maxHeight === '100%' ? '0%' : '100%'
    } else {
      element.menu.style.maxHeight = '0%'
    }
  })
}

 
elements.forEach(({ toggler }) => toggler.addEventListener("click", toggleCollapseMenu))
