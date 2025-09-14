//B1: tạo mảng chứa các sản phẩm

//B2: tạo HTML cho từng sản phẩm
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

//B3: chèn sản phẩm vào trang web
