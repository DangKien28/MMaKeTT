const email = document.getElementById("email")
const password = document.getElementById("password")
const login_btn = document.getElementById("login-btn")
const login_form = document.getElementById("login-form")
const message = document.getElementById("message-area")

inputs = [email, password]

function validate()
{
  let allFields = true
  for (let field of inputs)
  {
    if (field.value.trim()==='')
    {
      allFields = false
      break
    }
  }

  if (allFields)
  {
    login_btn.disabled = false
  }
  else
  {
    login_btn.disabled = true
  }
}

inputs.forEach(field => {
  field.addEventListener('input', validate)
})

login_form.addEventListener('submit', function(event) {
  event.preventDefault()
  fetch("/api/login", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(
      {
        "email": email.value,
        "password": password.value
      }
    )
  })
  .then(response => response.json())
  .then(result => {
    if (result["status"]==='not-register')
    {
      showMessage("The email has not been registered", "error")
    }
    else if (result["status"]==="success")
    {
      window.location.href = result["redirect_url"]
    }

    if (result["error"])
    {
      showMessage("Password is incorrect", "error")
    }

  })
})

function showMessage(mes, type) {
  message.innerHTML = `<p>${mes}</p>`;
  message.style.border = "solid 2px";
  message.style.borderRadius = "10px";
  message.style.padding = "10px";

  if (type === 'error') {
    message.style.borderColor = "red";
    message.style.backgroundColor = "#ffdddd";
    message.style.color = "#d8000c";
  } else if (type === 'success') {
    message.style.borderColor = "green";
    message.style.backgroundColor = "#d4edda";
    message.style.color = "#155724";
  }
}