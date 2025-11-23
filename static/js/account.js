document.addEventListener("DOMContentLoaded", function() {
  const menu = document.querySelector(".sidebar")
  const mainContent = document.getElementById("main-content")
  const defaultLink = document.getElementById("default-link")

  async function loadContent(url) {
    try {
      mainContent.innerHTML = '<p>Loading...</p>'

      const response = await fetch(url)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const html = await response.text()
      mainContent.innerHTML = html

      // --- SỬA ĐỔI TẠI ĐÂY ---
      // Kiểm tra URL để biết đang ở trang nào và chạy hàm xử lý tương ứng
      if (url.includes("/account/information")) {
        handleInformationPage();
      } else if (url.includes("/account/change-password")) {
        handleChangePasswordPage();
      }
      // ------------------------

    } catch (error) {
      mainContent.innerHTML = `<p>Error loading content: ${error.message}</p>`
      console.log("Fetch error: ", error)
    }
  }

  // Hàm riêng để xử lý logic cho trang Thông tin (Information)
  function handleInformationPage() {
    const username = document.getElementById('user-name')
    const email = document.getElementById("email")
    const dob = document.getElementById("dob")
    const gender = document.getElementById("gender")
    const phone_number = document.getElementById("phone")
    const address = document.getElementById("address")
    const id_card = document.getElementById("id-card")
    const doi = document.getElementById("date-issue")
    const poi = document.getElementById("place-issue")
    const save_btn = document.getElementById("save-btn")

    // Nếu không tìm thấy nút save (có thể do HTML chưa load xong hoặc sai trang), thoát luôn để tránh lỗi
    if (!save_btn) return;

    fetch("/api/basicInfo")
      .then(response => response.json())
      .then(data => {
        if(username) username.value = data["username"] || ""
        if(email) email.value = data["email"] || ""
        if(dob) dob.value = validateTime(data["date_of_birth"])
        if(gender) gender.value = data["gender"] || ""
        if(address) address.value = data["address"] || ""
        if(phone_number) phone_number.value = data["phone"] || ""
        if(id_card) id_card.value = data["id_card"] || ""
        if(doi) doi.value = validateTime(data["date_of_issue"])
        if(poi) poi.value = data["place_of_issue"] || ""
      })

    save_btn.addEventListener("click", function() {
      const data = {
        "username": username.value,
        "email": email.value,
        "birth": dob.value,
        "gender": gender.value,
        "address": address.value,
        "phone": phone_number.value,
        "id_card": id_card.value,
        "date_of_issue": doi.value,
        "place_of_issue": poi.value
      }
      fetch("/api/update_account", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
          alert(`${result["message"]}`)
        })
    })
  }

  // Hàm riêng để xử lý logic cho trang Đổi mật khẩu (Change Password)
  function handleChangePasswordPage() {
    console.log("Đang ở trang Change Password");
    // Sau này bạn sẽ viết code xử lý đổi mật khẩu ở đây
    // Ví dụ: Bắt sự kiện click cho nút 'Save' trong _change_password.html
  }

  menu.addEventListener('click', function(event) {
    const link = event.target.closest('a')
    if (!link) return

    event.preventDefault()

    const menuItem = link.parentElement

    if (menuItem.classList.contains('has-submenu')) {
      menuItem.classList.toggle('open')
      const submenu = menuItem.querySelector('.submenu')
      if (submenu) {
        submenu.style.display = menuItem.classList.contains('open') ? 'block' : 'none'
      }
    }

    const url = link.dataset.url
    if (url) {
      const allLinks = menu.querySelectorAll('a[data-url]')
      allLinks.forEach(l => l.classList.remove('active'))
      link.classList.add('active')
      loadContent(url)
    }
  })

  if (defaultLink) {
    const defaultUrl = defaultLink.dataset.url
    loadContent(defaultUrl)
  }
})

function validateTime(time) {
  if (!time) return ""; // Kiểm tra nếu time null thì trả về rỗng
  const realTime = new Date(time)
  const date = realTime.getDate()
  const month = realTime.getMonth() + 1
  const year = realTime.getFullYear()

  const dayStr = String(date).padStart(2, '0');
  const monthStr = String(month).padStart(2, '0');

  return `${year}-${monthStr}-${dayStr}`
}