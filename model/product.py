from . import get_db_connection

class Product:
  def __init__(self, name, price, rating, image_url):
    self.name = name
    self.price = price
    self.rating = rating
    self.image_url = image_url
  
  def save_product(self):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(
      "INSERT INTO products (product_name, product_price, product_rating, image_url) VALUES (%s, %s, %s, %s)",
      (self.name, self.price, self.rating, self.image_url)
    )
    db.commit()
    db.close()

def all_products():
  db = get_db_connection()
  cursor = db.cursor(dictionary=True)
  cursor.execute("SELECT * FROM products")
  products_data = cursor.fetchall()
  db.close()
  producs_list = []
  for p_data in products_data:
    product = Product(
      name=p_data["product_name"],
      price=p_data["product_price"],
      rating=p_data["product_rating"],
      image_url=p_data["image_url"]
    )
    producs_list.append(product)
  return producs_list
  
