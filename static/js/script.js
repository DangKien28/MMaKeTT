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
                        <a href="#" class="btn btn-secondary">XEM CHI TIẾT</a>
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