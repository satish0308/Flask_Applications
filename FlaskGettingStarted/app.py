from flask import Flask

app=Flask(__name__)

@app.route('/')
@app.route("/home")
def home():
    return f"<h1> Welcome to your first web application</h1>"

@app.route("/name/<your_name>")
def name(your_name):
    return f"<h1> Welcome {your_name} to your first web application</h1>"

#@app.route("/addition_two/<int:num1>/<int:num2>")
@app.route("/add/<my_name>/<int:num1>/<int:num2>")
def add(my_name,num1,num2):
    return f"<h1> Welcome {my_name} to your first web application, sum of the num is {num1+num2} please click here to go home </h1>"


if __name__=='__main__':
    app.run(debug=True)