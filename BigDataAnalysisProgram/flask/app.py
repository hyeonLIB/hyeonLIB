from django.shortcuts import render
from flask import Flask, render_template
from flask import redirect, url_for 

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", content='Testing')

# # You can pass a parameter via url path with /> tag
# @app.route("/<name>")
# def user(name):
#     return f"Hello {name}!"

# @app.route("/home/<content>")
# def content(content):
#     return render_template("ind.html", content = content)

# # if some condition doesn't satisfy, it would redirect to home page                                 
# @app.route("/admin")
# def admin():
#     return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)