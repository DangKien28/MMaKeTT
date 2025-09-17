from . import get_db_connection
from datetime import date
from enum import Enum

class User:
  def __init__(self, name, email, phone, password, id = None):
    self.id = id
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
    self.id = cursor.lastrowid
    db.commit()
    db.close()

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

def find_user(email):
  db = get_db_connection()
  cursor = db.cursor(dictionary=True)
  cursor.execute(
    "SELECT * FROM users WHERE email=%s",
    (email,)
  )
  row = cursor.fetchone()
  db.close()
  if row:
    return User(id=row["id"], name=row["name"], email=row["email"], phone=row["phone"], password=row["password"])
  return None
  
class Gender(Enum):
  MALE = "Male"
  FEMALE = "Female"
  OTHER = "Other"

class Account:
  def __init__(self, birth, gender, address, id_card, date_of_issue, place_of_issue, id=None, user_id = None):
    self.id = id
    self.user_id = user_id
    self.birth = birth
    self.gender = gender
    self.address = address
    self.id_card = id_card
    self.date_of_issue = date_of_issue
    self.place_of_issue = place_of_issue

  def save_account(self):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(
      "INSERT INTO users_info (user_id, birth, gender, address, id_card, date_of_issue, place_of_issue) VALUES (%s, %s, %s, %s, %s, %s, %s)",
      (self.user_id, self.birth, self.gender.value, self.address, self.id_card, self.date_of_issue, self.place_of_issue) 
    )
    db.commit()
    db.close()

def find_by_id(user_id):
  db = get_db_connection()
  cursor = db.cursor(dictionary=True)
  cursor.execute(
    "SELECT * FROM users_info WHERE user_id=%s",
    (user_id,)
  )
  row = cursor.fetchone()
  db.close()

  if row:
    if row["gender"]:
      gender_enum = Gender(row["gender"])
    else:
      gender_enum = None
    return Account(
      user_id=row["user_id"],
      birth=row["birth"],
      gender=gender_enum,
      address=row["address"],
      id_card=row["id_card"],
      date_of_issue=row["date_of_issue"],
      place_of_issue=row["place_of_issue"]
    )
  return None

def update_account(user_id, name, email, phone):
  db = get_db_connection()
  cursor = db.cursor(dictionary=True)
  cursor.execute(
    "UPDATE users SET name = %s, email = %s, phone = %s WHERE id = %s",
    (name, email, phone, user_id)
  )
  db.commit()
  db.close()
  return True

def update_account_info(user_id, data):
  db = get_db_connection()
  cursor = db.cursor(dictionary=True)
  cursor.execute(
    "UPDATE users_info SET birth = %s, gender = %s, address = %s, id_card = %s, date_of_issue = %s, place_of_issue = %s WHERE user_id = %s",
    (
      data["birth"], data["gender"], data["address"], data["id_card"], data["date_of_issue"], data["place_of_issue"], user_id
    )
  )
  db.commit()
  db.close()
  return True