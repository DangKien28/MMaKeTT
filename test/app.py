from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)

@app.route('/register', methods = ["POST", "GET"])
def register():
  if request.method=="POST":
    data = request.get_data()
    print(data)
    return data
  return render_template("index.html")
if __name__=="__main__":
  app.run(debug=True)