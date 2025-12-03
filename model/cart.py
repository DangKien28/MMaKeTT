from . import get_db_connection
class CartItem:
    def __init__(self, product_id, quantity, name=None, price=0, image_url=None):
        self.product_id = product_id 
        self.quantity = quantity
        self.name = name
        self.price = price
        self.image_url = image_url

    def total_price(self):
        return self.price * self.quantity

# Class đại diện cho Giỏ hàng
class Cart:
    def __init__(self, user_id):
        self.user_id = user_id 
        self.cartList = []     

    def load_from_db(self):
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        query = """
            SELECT c.product_id, c.quantity, p.product_name, p.product_price, p.image_url
            FROM cart c
            JOIN products p ON c.product_id = p.id
            WHERE c.user_id = %s
        """
        cursor.execute(query, (self.user_id,))
        rows = cursor.fetchall()

        self.cartList = []
        for row in rows:
            item = CartItem(
                product_id=row['product_id'],
                quantity=row['quantity'],
                name=row['product_name'],
                price=row['product_price'],
                image_url=row['image_url']
            )
            self.cartList.append(item)
        db.close()

    def save_item_to_db(self, product_id, quantity):
        db = get_db_connection()
        cursor = db.cursor() 
        query = "SELECT id, quantity FROM cart WHERE user_id=%s AND product_id=%s"
        cursor.execute(query, (self.user_id, product_id))
        row = cursor.fetchone()

        if row:
            new_quantity = row[1] + quantity 
            cursor.execute("UPDATE cart SET quantity=%s WHERE id=%s", (new_quantity, row[0]))
        else:
            print(self.user_id, product_id, quantity)
            cursor.execute("INSERT INTO cart (user_id, product_id, quantity) VALUES(%s, %s, %s)", (self.user_id, product_id, quantity))
        db.commit()
        db.close()

    # Hàm xóa khỏi DB
    def remove_item_from_db(self, product_id):
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM cart WHERE user_id=%s AND product_id=%s", (self.user_id, product_id))
        db.commit()
        db.close()