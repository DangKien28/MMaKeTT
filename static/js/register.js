document.addEventListener('DOMContentLoaded', function() {
  const sendcodeBtn = document.getElementById('send-code-btn')
  const verifyBtn = document.getElementById('verify-code-btn')
  const registerBtn = document.getElementById('register-btn')
  const emailInput = document.getElementById('email')
  const codeInput = document.getElementById('code-input')
  const messageArea = document.getElementById('message-area')
  const registerForm = document.getElementById('register-form')

  codeInput.addEventListener('input', ()=>{
    if (codeInput.value.trim() != '')
    {
      verifyBtn.disabled = false
    }
    else
    {
      verifyBtn.disabled = true
    }
  })

  //Sự kiện khi bấm nút "Send code"
  sendcodeBtn.addEventListener('click', async () => {
    const email = emailInput.value
    if (!email) {
     showMessage("Vui lòng nhập email!", "danger")
     return 
    }
    showMessage("Đang gửi mã...", "info")
    sendcodeBtn.disabled = true

    try {
      const response = await fetch('/send-verification-code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email }),
      });
      const data = await response.json();
      showMessage(data.message, response.ok ? 'success' : 'danger');
    } catch (error) {
        showMessage('Lỗi kết nối. Vui lòng thử lại.', 'danger');
    } finally {
        sendcodeBtn.disabled = false; // Kích hoạt lại nút sau khi hoàn tất
    }
  })

  verifyBtn.addEventListener('click', async () => {
    const code = codeInput.value
    try {
      const response = await fetch('/verify-code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: code }),
    });

    const data = await response.json();
    if (response.ok) {
        showMessage(data.message, 'success');
                // Kích hoạt nút đăng ký và khóa các trường đã xác thực
        registerBtn.disabled = false;
        emailInput.readOnly = true;
        codeInput.readOnly = true;
        sendcodeBtn.disabled = true;
        verifyBtn.disabled = true;
    } else {
        showMessage(data.message, 'danger');
    }
    } catch (error) {
        showMessage('Lỗi kết nối. Vui lòng thử lại.', 'danger');
    }

  })



  registerForm.addEventListener('submit', (event)=>{
    if (registerBtn.disabled)
    {
      event.preventDefault()
      showMessage("Vui lòng đợi hoàn tất xác thực email trước khi đăng ký", 'warning')
    }
  })

  registerBtn.addEventListener('click', (event)=>{
    const password = document.getElementById('password').value
    const confirm = document.getElementById('confirm-password').value
    
    if (password!=confirm)
    {
      showMessage('Xác nhận mật khẩu không khớp', 'danger')
      event.preventDefault()
    }
  })

  //Hàm hiển thị thông báo
  function showMessage(message, type) {
    messageArea.innerHTML = `<div class = "alert alert-${type}" role="alert">${message}</div>`
  }
})