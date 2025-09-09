from flask import session

def login_user(user):
  session["username"] = user.name
  session["email"] = user.email

def logout_user():
    session.pop("username", None)
    session.pop("email", None)
  
def is_logged_in():
    return "username" in session