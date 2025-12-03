document.addEventListener('DOMContentLoaded', function(){
  const productsContainer = document.getElementById('product-container');
  fetch('api/products')
  .then(response => response.json())
  .then(products => {
    if (products.length === 0)
    {
      productsContainer.innerHTML = '<p>No Product</p>';
      return;
    }

    productsContainer.innerHTML = '';

    products.forEach(product => {
      const productCardHTML = `
              <div class="product-card">
                <div class="product-image">
                    <div class="sale-badge"></div>
                    <div class="product-box"></div>
                </div>
                <div class="product-info">
                    <div class="product-name">${product.name}</div>
                    <div class="product-price">${product.price}</div>
                    <div class="product-rating">${product.rating}/5⭐️</div>
                    <div class="product-buttons">
                        <a href="#" class="btn btn-primary">MUA NGAY</a>
                        <button onclick="addToCart(${product.id})" class="btn btn-secondary" style="cursor: pointer;">Thêm vô giỏ hàng </button>
                    </div>
                </div>
            </div>
      `;
      productsContainer.insertAdjacentHTML('beforeend', productCardHTML)
    })
  })
  .catch(error => {
    console.error('Lỗi khi lấy dữ liệu sản phẩm: ', error);
    productsContainer.innerHTML = '<p>Có lỗi khi tải sản phẩm</p>'
  })

  //Ấn nút tìm kiếm
  const search_btn = document.getElementById('search_icon')
  if (search_btn)
  {
    search_btn.addEventListener('click', search_product)
  }

})

function search_product()
{
  const search_input = document.getElementById("search_input").value

  
}

async function addToCart(productId) {
    try {
        const response = await fetch('/api/cart/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "product_id": productId })
        });

        if (response.status === 401) {
            alert("Vui lòng đăng nhập để mua hàng!");
            window.location.href = "/login"; // Chuyển hướng đến trang đăng nhập
            return;
        }

        const data = await response.json();
        
        if (response.ok) {
            alert("✅ " + data.message);
            
        } else {
            alert("❌ Lỗi: " + data.message);
        }

    } catch (error) {
        console.error('Error:', error);
        alert("Có lỗi xảy ra khi thêm vào giỏ hàng.");
    }
}