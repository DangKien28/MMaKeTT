function showAlert(msg, type='danger') {
        const el = document.getElementById('alert-msg');
        el.className = `alert alert-${type}`;
        el.innerText = msg;
        el.classList.remove('d-none');
    }

    async function sendCode() {
        const email = document.getElementById('fp-email').value;
        if(!email) return showAlert("Vui lòng nhập email");

        try {
            const res = await fetch('/api/forgot-password/send-code', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({email: email})
            });
            const data = await res.json();
            
            if(res.ok) {
                showAlert(data.message, 'success');
                document.getElementById('step-1').classList.remove('active');
                document.getElementById('step-2').classList.add('active');
            } else {
                showAlert(data.message);
            }
        } catch (e) { showAlert("Lỗi kết nối"); }
    }

    async function verifyCode() {
        const code = document.getElementById('fp-code').value;
        if(!code) return showAlert("Vui lòng nhập mã");

        try {
            const res = await fetch('/api/forgot-password/verify-code', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({code: code})
            });
            const data = await res.json();
            
            if(res.ok) {
                showAlert(data.message, 'success');
                document.getElementById('step-2').classList.remove('active');
                document.getElementById('step-3').classList.add('active');
            } else {
                showAlert(data.message);
            }
        } catch (e) { showAlert("Lỗi kết nối"); }
    }

    async function resetPassword() {
        const password = document.getElementById('fp-new-pass').value;
        if(!password) return showAlert("Vui lòng nhập mật khẩu mới");

        try {
            const res = await fetch('/api/forgot-password/reset', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({password: password})
            });
            const data = await res.json();
            
            if(res.ok) {
                alert("Đổi mật khẩu thành công! Vui lòng đăng nhập lại.");
                window.location.href = "/login";
            } else {
                showAlert(data.message);
            }
        } catch (e) { showAlert("Lỗi kết nối"); }
    }