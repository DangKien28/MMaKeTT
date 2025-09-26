document.addEventListener("DOMContentLoaded", function() {
  const menu = document.querySelector(".sidebar")
  const mainContent = document.getElementById("main-content")
  const defaultLink = document.getElementById("default-link")

  async function loadContent(url)
  {
    try
    {
      mainContent.innerHTML = '<p>Loading...</p>'

      const response = await fetch(url)
      if (!response.ok)
      {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const html = await response.text()
      mainContent.innerHTML = html
    }
    catch (error)
    {
      mainContent.innerHTML = `<p>Error loading content: ${error.message}</p>`
      console.log("Fetch error: ", error)
    }
  }

  menu.addEventListener('click', function (event) {
    const link = event.target.closest('a')
    if (!link) return

    event.preventDefault()

    const menuItem = link.parentElement

    if (menuItem.classList.contains('has-submenu'))
    {
      menuItem.classList.toggle('open')
      const submenu = menuItem.querySelector('.submenu')
      if (submenu)
      {
        submenu.style.display = menuItem.classList.contains('open')?'block':'none'
      }
    }

    const url = link.dataset.url
    if (url)
    {
      const allLinks = menu.querySelectorAll('a[data-url]')
      allLinks.forEach(l=> l.classList.remove('active'))
      link.classList.add('active')
      loadContent(url)
    }
  })

  if (defaultLink)
  {
    const defaultUrl = defaultLink.dataset.url
    loadContent(defaultUrl)
  }
})