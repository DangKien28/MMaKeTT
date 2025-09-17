/**
 * Hàm hiển thị toast notification
 * @param {string} message - Nội dung thông báo
 * @param {string} type - Loại thông báo ('success' hoặc 'error')
 */

document.addEventListener('DOMContentLoaded', function(){
  fetch('/api/account')
  .then(response => {return response.json()})
  .then(data => {
    document.getElementById('username').value = data.username
    document.getElementById('email').value = data.email
    document.getElementById('phone').value = data.phone
    document.getElementById('date_of_birth').value = Format(data.birth)
    document.getElementById('gender').value = data.gender
    document.getElementById('address').value = data.address
    document.getElementById('id_card').value = data.id_card
    document.getElementById('date_of_issue').value = Format(data.date_of_issue)
    document.getElementById('place_of_issue').value = data.place_of_issue
  })
  .catch(error => {
    console.error("Lỗi khi truy xuất json", error)
  })


  //Thực hiện hành động khi ấn nút Save
  const save_btn = document.getElementById('save_btn')

  if (save_btn)
  {
    save_btn.addEventListener('click', save_account_info)
  }
})

function Format(dateInput) {
  const dateObj = new Date(dateInput)

  const year = dateObj.getFullYear()
  const month = String(dateObj.getMonth()+1).padStart(2, '0')
  const day = String(dateObj.getDate()).padStart(2, '0')

  return `${year}-${month}-${day}`
}

//hàm thực hiện hành động
function save_account_info() {
  console.log("Thực hiện hành động lưu")
  const account_data = {
    username: document.getElementById("username").value,
    email: document.getElementById("email").value,
    birth: document.getElementById("date_of_birth").value,
    gender: document.getElementById("gender").value,
    phone: document.getElementById("phone").value,
    address: document.getElementById("address").value,
    id_card: document.getElementById("id_card").value,
    date_of_issue: document.getElementById("date_of_issue").value,
    place_of_issue: document.getElementById("place_of_issue").value
  }

  fetch("/api/account/update", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(account_data)
  })
  .then(response => response.json())
  .then(data => {
    if (data.status === 'success') {
      showToast(data.message, 'success')
    }
    else {
      showToast('Lỗi: '+data.message, 'error')
    }
  })
  .catch(error => {
    console.error("Xảy ra lỗi khi gửi yêu cầu: ", error)
    showToast("Không thể kết nối tới máy chủ", "error")
  })
}

function showToast(message, type='success')
{
  const container = document.getElementById('toastContainer')

  const toast = document.createElement('div')
  toast.classList.add('toast', `toast--${type}`)
  toast.innerText = message
  container.appendChild(toast)
  setTimeout(()=>{
    toast.classList.add('show')
  }, 100)

  setTimeout(()=>{
    toast.classList.remove('show')
    toast.addEventListener('transitioned', ()=>toast.remove())
  }, 3000)
}