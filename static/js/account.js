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
  function handleChangePasswordPage()
{
    console.log("Đã load js")
    console.log("Đang ở trang Change Password");

    const btnSendCode = document.getElementById("btn-send-code")
    const btnSave = document.getElementById("btn-save-password")
    const codeInput = document.getElementById("code-input")
    const newPassword = document.getElementById("new-password")
    const confirmPassword = document.getElementById("confirm-password")

    let userEmail=""

    fetch("/api/basicInfo")
    .then(res=>res.json())
    .then(data => {
        userEmail = data.email
        console.log("Email: ", userEmail)
    })
    .catch(err=>console.error("Không lấy được email: lỗi ", err))


    //Nut Send Code
    btnSendCode.addEventListener("click", function() {
        if (!userEmail)
        {
            console.log("Khong tim thay email")
            return
        }

        btnSendCode.innerText = "sending";
        btnSendCode.disabled = true

        fetch("/send-verification-code", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({email: userEmail})
        })
        .then(res => {
            if (res.ok)
            {
                alert("đã gửi mã xác thực tới email: "+userEmail)
            }
            else
            {
                alert("Gui ma that bai")
            }
        })
        .catch(err=>alert("Loi ket noi"))
        .finally(()=> {
            btnSendCode.innerText="Send Code"
            btnSendCode.disabled = false
        })
    })

    //Nut Save
    btnSave.addEventListener("click", function() {
        const code = codeInput.value.trim()
        const new_password = newPassword.value
        const confirm = confirmPassword.value

        if (!code) return alert("Vui lòng nhập mã xác thực.");
        if (!new_password) return alert("Vui lòng nhập mật khẩu mới.");
        if (new_password !== confirm) return alert("Mật khẩu xác nhận không khớp.");

        fetch("/api/change-password", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(
                {
                    code: code,
                    new_password: new_password
                }
            )
        })
        .then(res=>res.json())
        .then(data => {
            if (data.status ==="success")
            {
                alert(data.message)
                window.location.href = "/login"
            }
            else
            {
                alert("Lỗi: "+data.message)
            }
        })
        .catch(err=>console.error("Lỗi: ", err))
    })
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

