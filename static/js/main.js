document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('search-button')) initHomePage();
    if (document.getElementById('admin-shop-list')) loadAdminShops();
    if (document.getElementById('cart-items-container')) loadCart();
    if (document.getElementById('checkout-items')) initCheckoutPage();
    
    loadNotifications();
    
    if (document.getElementById('seller-noti-list')) {
        loadSellerNotifications();
        setInterval(loadSellerNotifications, 5000);
    }

    if (typeof ORDER_ID !== 'undefined') initOrderSuccessPage();
});

function initHomePage() {
    const searchBtn = document.getElementById('search-button');
    searchBtn.addEventListener('click', fetchProducts);
    
    fetchProducts(); 
    fetchSuggestions();
}

async function fetchProducts() {
    try {
        const keyword = document.getElementById('keyword').value;
        const vendor = document.getElementById('vendor-filter').value;
        const category = document.getElementById('category-filter').value;

        const res = await fetch(`/api/products?keyword=${keyword}&vendor=${vendor}&category=${category}`);
        const data = await res.json();
        
        const container = document.getElementById('product-results');
        container.innerHTML = '';
        document.getElementById('result-count').innerText = `Tìm thấy ${data.count} sản phẩm:`;

        if (data.products.length === 0) {
            container.innerHTML = '<p>Không tìm thấy sản phẩm nào.</p>';
            return;
        }

        data.products.forEach(p => {
            container.innerHTML += renderProductCardHTML(p);
        });
    } catch (e) { console.error(e); }
}

function renderProductCardHTML(p) {
    return `
        <div class="product-card">
            <h4><a href="/product/${p.id}" style="text-decoration:none; color:#2c3e50;">${p.name}</a></h4>
            <p class="product-price">${p.price.toLocaleString()} đ</p>
            <p>Hãng: ${p.vendor}</p>
            <div style="margin-top: 10px;">
                <button onclick="addToCart('${p.id}')" class="action-btn secondary" style="width:100%; padding: 5px;">+ Thêm vào giỏ</button>
                <a href="/product/${p.id}" style="display:block; text-align:center; margin-top:8px; font-size:13px; color:#3498db; text-decoration:none;">Xem chi tiết >></a>
            </div>
        </div>`;
}

async function fetchSuggestions() {
    try {
        const res = await fetch('/api/suggestions');
        const data = await res.json();
        renderList(data.behavioral, 'behavioral-list');
        renderList(data.trending, 'trending-list');
    } catch (e) { console.error(e); }
}

function renderList(products, elementId) {
    const el = document.getElementById(elementId);
    if (el && products.length > 0) {
        el.innerHTML = products.map(p => renderProductCardHTML(p)).join('');
    }
}
let currentProduct = null;
let selectedVariantId = null;

async function addToCart(productId) {
    try {
        const res = await fetch(`/api/product/${productId}`);
        const product = await res.json();
        
        if (product.variants && product.variants.length > 0) {
            openProductModal(product); 
        } else {
            submitAddToCart(productId, 1, null); 
        }
    } catch (e) { console.error(e); }
}

function openProductModal(product) {
    currentProduct = product;
    selectedVariantId = null;

    document.getElementById('modal-p-name').innerText = product.name;
    document.getElementById('modal-p-price').innerText = product.price.toLocaleString() + ' đ';
    document.getElementById('modal-qty').value = 1;
    document.getElementById('stock-status').innerText = "";
    
    const container = document.getElementById('variant-options');
    container.innerHTML = '';
    
    product.variants.forEach(v => {
        const btn = document.createElement('button');
        btn.className = 'variant-btn';
        btn.innerText = v.name;
        if (v.stock <= 0) {
            btn.classList.add('disabled');
            btn.innerText += " (Hết)";
            btn.disabled = true;
        } else {
            btn.onclick = () => {
                selectedVariantId = v.id;
                document.querySelectorAll('.variant-btn').forEach(b => b.classList.remove('selected'));
                btn.classList.add('selected');
                document.getElementById('stock-status').innerText = `Kho: ${v.stock}`;
            };
        }
        container.appendChild(btn);
    });
    document.getElementById('product-modal').classList.remove('hidden');
}

if(document.querySelector('.close-modal')) {
    document.querySelector('.close-modal').onclick = () => document.getElementById('product-modal').classList.add('hidden');
}

if(document.getElementById('confirm-add-btn')) {
    document.getElementById('confirm-add-btn').onclick = () => {
        if (!selectedVariantId) return alert("Vui lòng chọn phân loại!");
        const qty = document.getElementById('modal-qty').value;
        submitAddToCart(currentProduct.id, qty, selectedVariantId);
        document.getElementById('product-modal').classList.add('hidden');
    };
}

async function submitAddToCart(productId, qty, variantId) {
    try {
        const res = await fetch('/api/cart/add', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ product_id: productId, qty: qty, variant_id: variantId })
        });
        const data = await res.json();
        showToast(data.message, !data.success);
    } catch (e) { showToast("Lỗi kết nối!", true); }
}

function showToast(message, isError = false) {
    const toast = document.getElementById('toast');
    if(toast) {
        toast.innerText = message;
        toast.className = isError ? 'toast error show' : 'toast show';
        setTimeout(() => toast.classList.remove('show'), 3000);
    }
}

async function loadCart() {
    try {
        const res = await fetch('/api/cart');
        const data = await res.json();
        
        document.getElementById('subtotal').innerText = data.subtotal.toLocaleString() + ' đ';
        document.getElementById('shipping').innerText = data.shipping_fee.toLocaleString() + ' đ';
        document.getElementById('discount').innerText = '-' + data.discount.toLocaleString() + ' đ';
        document.getElementById('final-total').innerText = data.final_total.toLocaleString() + ' đ';

        const container = document.getElementById('cart-items-container');
        if (data.items.length === 0) {
            container.innerHTML = '<p>Giỏ hàng trống.</p>';
            return;
        }
        
        container.innerHTML = data.items.map(item => `
            <div class="cart-item" style="border-bottom:1px solid #eee; padding:10px 0; display:flex; justify-content:space-between;">
                <div>
                    <b>${item.product.name}</b>
                    ${item.variant_name ? `<br><small>Phân loại: ${item.variant_name}</small>` : ''}
                    <br><span style="color:red">${item.total_price.toLocaleString()} đ</span>
                </div>
                <div style="display:flex; align-items:center; gap:5px;">
                    <button onclick="updateCartItem('${item.product.id}', -1)">-</button>
                    <span>${item.qty}</span>
                    <button onclick="updateCartItem('${item.product.id}', 1)">+</button>
                    <button onclick="removeCartItem('${item.product.id}')" style="margin-left:10px; color:red; border:none; background:none; cursor:pointer;">Xóa</button>
                </div>
            </div>
        `).join('');
    } catch (e) { console.error(e); }
}

async function updateCartItem(pid, change) {
    await fetch('/api/cart/update', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ product_id: pid, change: change })
    });
    loadCart();
}

async function removeCartItem(pid) {
    if(!confirm('Xóa sản phẩm này?')) return;
    await fetch('/api/cart/remove', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ product_id: pid })
    });
    loadCart();
}


async function initCheckoutPage() {
    try {
        const res = await fetch('/api/cart');
        const data = await res.json();
        if(data.items.length === 0) { alert('Giỏ hàng trống!'); window.location.href='/'; return; }

        document.getElementById('checkout-items').innerHTML = data.items.map(i => `
            <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                <span>${i.product.name} (x${i.qty})</span>
                <span>${i.total_price.toLocaleString()} đ</span>
            </div>`).join('');
        
        document.getElementById('co-total').innerText = data.final_total.toLocaleString() + ' đ';
        document.getElementById('co-subtotal').innerText = data.subtotal.toLocaleString() + ' đ';
        document.getElementById('co-discount').innerText = data.discount.toLocaleString() + ' đ';
        document.getElementById('co-shipping').innerText = data.shipping_fee.toLocaleString() + ' đ';
    } catch(e) {}
}

async function submitOrder() {
    const name = document.getElementById('cust-name').value;
    const phone = document.getElementById('cust-phone').value;
    const address = document.getElementById('cust-address').value;
    const method = document.querySelector('input[name="payment"]:checked').value;

    if(!name || !phone || !address) return alert("Vui lòng điền đủ thông tin!");

    const res = await fetch('/api/order/create', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ name, phone, address, payment_method: method })
    });
    const result = await res.json();
    if(result.success) window.location.href = `/order-success/${result.order_id}`;
    else alert(result.message);
}

async function initOrderSuccessPage() {
    try {
        const res = await fetch(`/api/order/${ORDER_ID}`);
        const order = await res.json();
        if(order.error) return;

        document.getElementById('display-order-id').innerText = ORDER_ID;
        document.getElementById('order-details-box').classList.remove('hidden');
        document.getElementById('od-name').innerText = order.customer.name;
        document.getElementById('od-address').innerText = order.customer.address;
        document.getElementById('od-total').innerText = order.financials.total.toLocaleString() + ' đ';
        document.getElementById('od-items').innerHTML = order.items.map(i => `<div>${i.product.name} x${i.qty}</div>`).join('');
    } catch(e) {}
}



async function registerShop() {
    const name = document.getElementById('reg-name').value;
    const email = document.getElementById('reg-email').value;
    if(!name) return alert("Nhập tên!");
    
    const res = await fetch('/api/shop/register', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ owner_name: name, email: email })
    });
    const data = await res.json();
    alert(data.message);
    if(data.shop) {
        document.getElementById('register-section').classList.add('hidden');
        document.getElementById('dashboard-section').classList.remove('hidden');
        loadSellerNotifications();
    }
}

async function loadAdminShops() {
    const res = await fetch('/api/admin/shops');
    const shops = await res.json();
    const container = document.getElementById('admin-shop-list');
    container.innerHTML = shops.map(s => `
        <tr>
            <td>${s.id}</td>
            <td>${s.owner_name}</td>
            <td>${s.status}</td>
            <td>
                ${s.status === 'pending' ? `<button onclick="approveShop('${s.id}', 'approve')">Duyệt</button>` : ''}
            </td>
        </tr>
    `).join('');
}

async function approveShop(id, action) {
    await fetch('/api/admin/approve', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ id: id, action: action })
    });
    loadAdminShops();
}

async function loadSellerNotifications() {
    const list = document.getElementById('seller-noti-list');
    const badge = document.getElementById('seller-noti-badge');
    if(!list) return;

    const res = await fetch('/api/seller/notifications');
    const data = await res.json();
    
    if(data.unread_count > 0) {
        badge.innerText = data.unread_count;
        badge.classList.remove('hidden');
    } else badge.classList.add('hidden');

    list.innerHTML = data.notifications.length ? data.notifications.map(n => `
        <div class="noti-item ${n.is_read ? '' : 'unread'}">
            <b>${n.title}</b><br>${n.message}
        </div>`).join('') : '<div style="padding:10px">Không có tin mới</div>';
}

async function toggleSellerNoti() {
    const drop = document.getElementById('seller-noti-dropdown');
    drop.classList.toggle('show');
    if(drop.classList.contains('show')) {
        await fetch('/api/seller/notifications/read', { method: 'POST' });
        document.getElementById('seller-noti-badge').classList.add('hidden');
    }
}

async function testSellerNoti(type) {
    const res = await fetch('/api/seller/test-noti', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ type })
    });
    const data = await res.json();
    alert(data.message);
    loadSellerNotifications();
}



async function loadNotifications() {
    const list = document.getElementById('noti-list');
    const badge = document.getElementById('noti-badge');
    if(!list) return;

    const res = await fetch('/api/notifications');
    const data = await res.json();

    if(data.unread_count > 0) {
        badge.innerText = data.unread_count;
        badge.classList.remove('hidden');
    } else badge.classList.add('hidden');

    list.innerHTML = data.notifications.length ? data.notifications.map(n => `
        <div class="noti-item ${n.is_read ? '' : 'unread'}">
            <b>${n.title}</b><br>${n.message}
        </div>`).join('') : '<div style="padding:10px">Trống</div>';
}

async function toggleNoti() {
    const drop = document.getElementById('noti-dropdown');
    drop.classList.toggle('show');
    if(drop.classList.contains('show')) {
        await fetch('/api/notifications/read', { method: 'POST' });
        document.getElementById('noti-badge').classList.add('hidden');
    }
}


function changeImage(src) {
    document.getElementById('main-img').src = src;
}

function zoomImage(event) {
    const img = document.getElementById('main-img');
    const rect = event.currentTarget.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    img.style.transformOrigin = `${x}px ${y}px`;
    img.style.transform = "scale(2)";
}

function resetZoom() {
    document.getElementById('main-img').style.transform = "scale(1)";
}

function toggleVideo() {
    document.getElementById('video-box').classList.toggle('hidden');
}

let detailSelectedVariantId = null;
function selectDetailVariant(vId, btn, stock) {
    detailSelectedVariantId = vId;
    document.querySelectorAll('#detail-variants .variant-btn').forEach(b => b.classList.remove('selected'));
    btn.classList.add('selected');
    document.getElementById('detail-stock').innerText = `Kho: ${stock}`;
}

async function addToCartFromDetail(productId) {
    if (typeof hasVariants !== 'undefined' && hasVariants && !detailSelectedVariantId) {
        return alert("Vui lòng chọn phân loại hàng!");
    }
    const qty = document.getElementById('detail-qty').value;
    submitAddToCart(productId, qty, detailSelectedVariantId);
}


let newAvatarBase64 = null; // Biến tạm lưu ảnh mới

function initProfilePage() {
    const fileInput = document.getElementById('file-input');
    if (fileInput) {
        fileInput.addEventListener('change', handleFileSelect);
    }
}

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (!file) return;

    const validTypes = ['image/jpeg', 'image/png', 'image/jpg'];
    if (!validTypes.includes(file.type)) {
        alert("Chỉ chấp nhận file ảnh JPG hoặc PNG!");
        return;
    }
    if (file.size > 2 * 1024 * 1024) { // 2MB
        alert("Dung lượng ảnh quá lớn! Vui lòng chọn ảnh dưới 2MB.");
        return;
    }

    const reader = new FileReader();
    reader.onload = function(e) {
        newAvatarBase64 = e.target.result; 
        document.getElementById('avatar-img').src = newAvatarBase64; 
    };
    reader.readAsDataURL(file);
}

async function saveProfile() {
    const name = document.getElementById('profile-name').value;
    const phone = document.getElementById('profile-phone').value;
    const address = document.getElementById('profile-address').value;

    if (!name || !phone) return alert("Vui lòng điền tên và số điện thoại!");

    try {
        const payload = {
            name: name,
            phone: phone,
            address: address
        };
        if (newAvatarBase64) {
            payload.avatar = newAvatarBase64;
        }

        const res = await fetch('/api/user/update', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });
        
        const data = await res.json();
        
        if (data.success) {
            showToast("Cập nhật hồ sơ thành công!");
        } else {
            alert(data.message);
        }
    } catch (e) {
        console.error(e);
        alert("Lỗi kết nối server!");
    }
}

async function loadOrderHistory() {
    const tbody = document.getElementById('order-history-list');
    if (!tbody) return;

    try {
        const res = await fetch('/api/my-orders');
        const orders = await res.json();

        if (orders.length === 0) {
            document.getElementById('empty-history').classList.remove('hidden');
            return;
        }

        tbody.innerHTML = orders.map(o => `
            <tr>
                <td><a href="/order-tracking/${o.id}" style="font-weight:bold; color:#3498db">${o.id}</a></td>
                <td>${o.created_at}</td>
                <td style="color:red; font-weight:bold">${o.financials.total.toLocaleString()} đ</td>
                <td>${translateStatus(o.status)}</td>
                <td>
                    <a href="/order-tracking/${o.id}" class="action-btn secondary" style="padding:5px 10px; text-decoration:none; font-size:12px">Chi tiết</a>
                </td>
            </tr>
        `).join('');

    } catch (e) { console.error(e); }
}

function translateStatus(status) {
    const map = {
        'pending': '<span style="color:orange">Chờ xác nhận</span>',
        'confirmed': '<span style="color:blue">Đã xác nhận</span>',
        'shipping': '<span style="color:purple">Đang giao</span>',
        'delivered': '<span style="color:green">Giao thành công</span>',
        'cancelled': '<span style="color:red">Đã hủy</span>'
    };
    return map[status] || status;
}

async function loadTrackingDetail() {
    if (typeof TRACKING_ORDER_ID === 'undefined') return;

    try {
        const res = await fetch(`/api/order/${TRACKING_ORDER_ID}`);
        const order = await res.json();

        if (order.error) return alert("Không tìm thấy đơn hàng!");

        document.getElementById('dt-id').innerText = order.id;
        document.getElementById('dt-name').innerText = order.customer.name;
        document.getElementById('dt-phone').innerText = order.customer.phone;
        document.getElementById('dt-address').innerText = order.customer.address;
        document.getElementById('dt-date').innerText = order.created_at;
        document.getElementById('dt-total').innerText = order.financials.total.toLocaleString() + ' đ';

        document.getElementById('dt-items').innerHTML = order.items.map(i => `
            <div style="border-bottom:1px solid #eee; padding:5px 0; display:flex; justify-content:space-between">
                <span>${i.product.name} x${i.qty}</span>
                <span>${i.total_price.toLocaleString()} đ</span>
            </div>
        `).join('');

        updateStepper(order.status);

    } catch (e) { console.error(e); }
}

function updateStepper(status) {
    ['pending', 'confirmed', 'shipping', 'delivered'].forEach(s => {
        document.getElementById(`step-${s}`).classList.remove('active');
    });

    if (status === 'pending') document.getElementById('step-pending').classList.add('active');
    if (status === 'confirmed') {
        document.getElementById('step-pending').classList.add('active');
        document.getElementById('step-confirmed').classList.add('active');
    }
    if (status === 'shipping') {
        document.getElementById('step-pending').classList.add('active');
        document.getElementById('step-confirmed').classList.add('active');
        document.getElementById('step-shipping').classList.add('active');
    }
    if (status === 'delivered') {
        document.querySelectorAll('.track-step').forEach(el => el.classList.add('active'));
    }
}

async function simulateStatus(newStatus) {
    if (!confirm(`Bạn có muốn chuyển đơn này sang trạng thái: ${newStatus}?`)) return;

    await fetch('/api/order/update-status', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ order_id: TRACKING_ORDER_ID, status: newStatus })
    });
    
    alert("Cập nhật thành công! Kiểm tra thông báo nhé.");
    loadTrackingDetail();
    loadNotifications();
}