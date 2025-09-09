from . import get_db_connection

class User:
  def __init__(self, name, email, phone, password):
    self.name = name
    self.email = email
    self.phone = phone
    self.password = password

  def save(self):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(
      "INSERT INTO users (name, email, phone, password) VALUES (%s, %s, %s, %s)",
      (self.name, self.email, self.phone, self.password)
    )
    db.commit()
    db.close()

  def find_user(self):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
      "SELECT * FROM users WHERE email=%s AND password=%s",
      (self.email, self.password)
    )
    row = cursor.fetchone()
    db.close()
    if row:
      return User(name=row["name"], email=row["email"], phone=row["phone"], password=row["password"])
    return None
  
  def check_account(self):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(
      "SELECT * FROM users WHERE email=%s",
      (self.email,)
    )
    row = cursor.fetchone()
    db.close()
    return row is not None
    