document.addEventListener("DOMContentLoaded", () => {
    loadCart();
});

async function loadCart() {
    const container = document.getElementById("cart-items-container");
    
    try {
        const response = await fetch('/api/cart/items');
        
        if (response.status === 401) {
            window.location.href = "/auth/login";
            return;
        }

        const items = await response.json();

        // 1. Kiểm tra nếu giỏ hàng trống
        if (!items || items.length === 0) {
            container.innerHTML = `
                <div style="text-align:center; padding: 20px;">
                    <p>Giỏ hàng của bạn đang trống.</p>
                    <a href="/" class="btn-primary" style="text-decoration:none;">Mua sắm ngay</a>
                </div>`;
            updateSummary(0); // Gọi hàm updateSummary
            return;
        }

        // 2. Tạo bảng hiển thị sản phẩm
        let html = `
            <table class="cart-table" style="width:100%; text-align:left; border-collapse: collapse;">
                <thead>
                    <tr style="border-bottom: 1px solid #ddd;">
                        <th style="padding:10px;">Sản phẩm</th>
                        <th>Đơn giá</th>
                        <th>Số lượng</th>
                        <th>Thành tiền</th>
                        <th>Hành động</th>
                    </tr>
                </thead>
                <tbody>
        `;

        let totalCartValue = 0;

        items.forEach(item => {
            totalCartValue += item.total; 

            html += `
                <tr style="border-bottom: 1px solid #eee;">
                    <td class="product-col" style="padding:10px; display:flex; align-items:center; gap:10px;">
                        <img src="${item.image_url}" alt="${item.name}" class="cart-img" style="width:50px; height:50px; object-fit:cover;">
                        <span>${item.name}</span>
                    </td>
                    <td>${formatCurrency(item.price)}</td>
                    <td>
                        <span class="qty-badge" style="padding:0 10px;">${item.quantity}</span>
                    </td>
                    <td><strong>${formatCurrency(item.total)}</strong></td>
                    <td>
                        <button onclick="removeFromCart(${item.product_id})" class="btn-delete" style="color:red; cursor:pointer; border:none; background:none;">Xóa</button>
                    </td>
                </tr>
            `;
        });

        html += '</tbody></table>';
        container.innerHTML = html;

        // 3. Cập nhật phần tổng tiền bên phải
        updateSummary(totalCartValue); // Gọi hàm updateSummary

    } catch (error) {
        console.error('Error loading cart:', error);
        container.innerHTML = "<p>Không thể tải giỏ hàng. Vui lòng thử lại sau.</p>";
    }
}

async function removeFromCart(productId) {
    if (!confirm("Bạn có chắc chắn muốn xóa sản phẩm này?")) return;

    try {
        const response = await fetch(`/api/cart/remove/${productId}`, {
            method: 'DELETE'
        });

        const data = await response.json();

        if (response.ok) {
            loadCart(); 
        } else {
            alert("Lỗi: " + data.message);
        }

    } catch (error) {
        console.error('Error removing item:', error);
        alert("Không thể xóa sản phẩm.");
    }
}

// CÁC HÀM HỖ TRỢ (UTILS)
function formatCurrency(amount) {
    return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(amount);
}

// --- QUAN TRỌNG: ĐÃ BỎ COMMENT ĐOẠN NÀY ---
function updateSummary(subtotal) {
    const subtotalEl = document.getElementById("subtotal");
    const finalTotalEl = document.getElementById("final-total");
    const shippingEl = document.getElementById("shipping"); 

    if (subtotalEl) subtotalEl.innerText = formatCurrency(subtotal);
    
    // Giả sử phí ship
    let shippingFee = 0; 
    if (subtotal > 0) {
        shippingFee = 30000; 
        if (shippingEl) shippingEl.innerText = formatCurrency(shippingFee);
    } else {
        if (shippingEl) shippingEl.innerText = formatCurrency(0);
    }

    if (finalTotalEl) finalTotalEl.innerText = formatCurrency(subtotal + shippingFee);
}