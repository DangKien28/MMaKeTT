function handleChangePasswordPage()
{
    console.log("Đã load js")

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
                    newPass: new_password
                }
            )
        })
        .then(res=>res.json())
        .then(data => {
            if (data.status ==="success")
            {
                alert(data.message)
                window.location.href = "/auth/login"
            }
            else
            {
                alert("Lỗi: "+data.message)
            }
        })
        .catch(err=>console.error("Lỗi: ", err))
    })
}