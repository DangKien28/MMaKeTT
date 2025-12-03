function createProductElement(product)
{
  const productItem = document.createElement('div')
  productItem.classList.add('product-item')

  productItem.innerHTML = `
    <img src="${product_image}" alt="Hình ảnh sản phẩm">

    <div class="product-details">

      <h3 class="product-name">${product_name}</h3>

      <div class="rating">
        ${starsHtml}
      </div>

      <p class="price">${product_price}</p>

      <div class="buttons">
        <button class="buy-now-btn">Buy Now</button>
        <button class="add-to-cart-btn">Add to cart</button>
      </div>

    </div>
  `
  return productItem
}



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
})