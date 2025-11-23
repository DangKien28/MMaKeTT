const password = document.getElementById("password")
const confirm_password = document.getElementById("confirm-password")
const form = document.getElementById("register-form")
const message = document.getElementById("message-area")
const username = document.getElementById("username")
const email = document.getElementById("email")
const phone = document.getElementById("phone")
const send_code = document.getElementById("send-code-btn")
const code_input = document.getElementById("code-input")
const verify_code_btn = document.getElementById("verify-code-btn")
const register_btn = document.getElementById("register-btn")

const required = [username, email, phone, code_input, password, confirm_password]

function validateForm()
{
  let allFilled = true
  for (const field of required)
  {
    if (field.value.trim() === '')
    {
      allFilled = false
      break
    }
  }

  if (allFilled && password.value==confirm_password.value)
  {
    register_btn.disabled = false
  }
  else
  {
    register_btn.disabled = true
  }
}

email.addEventListener('input', function() {
  if (email.value.trim()==='')
  {
    send_code.disabled=true
  }
  else
  {
    send_code.disabled=false
  }
})

required.forEach(field => {
  field.addEventListener('input', validateForm)
})


email.addEventListener('blur', async () => {
  const email_value = email.value
  if (email_value)
  {
    const response = await fetch("/api/check_email", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({"email": email_value})
    })

    const data = await response.json()
    if (data.status_user===true)
    {
      message.innerHTML = '<p>❌Email đã được đăng ký</p>'
      message.style.backgroundColor = "orange"
      message.style.paddingTop = "15px"
      message.style.paddingBottom = "8px"
      message.style.border = "solid 2px red"
      message.style.borderRadius = "10px"
    }
    else
    {
      message.innerHTML = ''
      message.style.backgroundColor = ""
      message.style.paddingTop = ""
      message.style.paddingBottom = ""
      message.style.border = ""
      message.style.borderRadius = ""
    }

  }
})


form.addEventListener('submit', function(event) {
  if (email_value==null || email==null || phone==null || code_input==null || password==null || confirm_password==null)
  {
    send_code.disabled = true
    verify_code_btn.disabled = true
    register_btn.disabled = true
    message.innerHTML = "<p>Please type full fields</p>"
  }

  if (password.value!==confirm_password.value)
  {
    event.preventDefault()
    message.innerHTML = `<p>Xác nhận mật khẩu sai</p>`
    message.style.backgroundColor = "orange"
    message.style.paddingTop = "15px"
    message.style.paddingBottom = "8px"
    message.style.border = "solid 2px red"
    message.style.borderRadius = "10px"
  }
})

send_code.addEventListener('click', function() {
    fetch("/send-verification-code", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({"email": email.value})
    })
    .then(respone => respone.json())
    .then(result => {
      if (result["message"]==="failed")
      {
        message.innerHTML = "Error while sending verify code"
        message.style.backgroundColor = "orange"
        message.style.paddingTop = "15px"
        message.style.paddingBottom = "10px"
        message.style.border = "solid 2px red"
        message.style.borderRadius = "10px"
      }
      else
      {
        message.innerHTML = "Sent successfully"
        message.style.backgroundColor = "green"
        message.style.paddingTop = "15px"
        message.style.paddingBottom = "10px"
        message.style.border = "solid 2px blue"
        message.style.borderRadius = "10px"
      }
    })
})

phone.addEventListener("blur", function() {
  let phoneNum = phone.value
  let newPhone = phoneNum.replaceAll(' ', '')
  phone.value = newPhone
})

code_input.addEventListener('input', function() {
  if (code_input.value.trim().length >=6)
  {
    verify_code_btn.disabled = false
  }
})

verify_code_btn.addEventListener('click', function(){
  fetch("/verify-code", {
    method:"POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(
      {
        "email": email.value,
        "code": code_input.value
      }
    )
  })
  .then(respone => respone.json())
  .then(result => {
    if (result["message"]==="required")
    {
      message.innerHTML = "Please click 'Send code' button before doing this"
      message.style.backgroundColor = "orange"
      message.style.paddingTop = "15px"
      message.style.paddingBottom = "10px"
      message.style.border = "solid 2px red"
      message.style.borderRadius = "10px"
    }

    if (result["message"]==="Un-verify")
    {
      message.innerHTML = "Verify-code is not correct"
      message.style.backgroundColor = "orange"
      message.style.paddingTop = "15px"
      message.style.paddingBottom = "10px"
      message.style.border = "solid 2px red"
      message.style.borderRadius = "10px"
    }
    else
    {
      message.innerHTML = "Right verify-code"
      message.style.backgroundColor = "green"
      message.style.paddingTop = "15px"
      message.style.paddingBottom = "10px"
      message.style.border = "solid 2px blue"
      message.style.borderRadius = "10px"
    }
  })
})
