from enum import unique
from flask import Flask, redirect, render_template, request, flash, url_for
from flask_sqlalchemy import SQLAlchemy
import string
import random

app = Flask(__name__)
app.secret_key = "hello"

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:741222@localhost/test'

db=SQLAlchemy(app)

class Usersss(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    fname = db.Column (db.String(50), nullable=False)
    email = db.Column (db.String(50), unique=True, nullable=False)
    passwordsss = db.Column (db.String(50), nullable=False)

class Urls(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    long = db.Column (db.String(200), nullable=False)
    short = db.Column (db.String(4), nullable=False)


# Login

@app.route('/')
def index():
  return render_template('loging.html')

@app.route('/home', methods=["POST"])
def home():
      log_email = request.form.get("log_email")
      log_pass = request.form.get("log_pass")
      print(log_email)
      print(log_pass)
      log_details = Usersss.query.filter_by(email=log_email,passwordsss=log_pass).first()
      if log_details:
          return render_template('home.html', us_name=log_details.fname)
      else:
            flash("Invalid Email & Password")
            return render_template("loging.html")
        
# Register

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/succ',methods=["POST"])
def succ():

    names = request.form.get("name")
    emails = request.form.get("email")
    passwords = request.form.get("pass")
    print(names)
    print(emails)
    print(passwords)

    entry = Usersss(fname=names, email = emails, passwordsss=passwords)
    db.session.add(entry)
    db.session.commit()

    return render_template("loging.html")


# Create long Url to Short Url

def shorten_url():
    letters = string.ascii_lowercase + string.ascii_uppercase
    while True:
        rand_letters = random.choices(letters, k=4)
        rand_letters = "".join(rand_letters)
        short_url = Urls.query.filter_by(short=rand_letters).first()
        if not short_url:
            return rand_letters
            

@app.route('/shorted', methods=["POST"])
def shorted():
    real_url = request.form.get("inp_url")
    found_url = Urls.query.filter_by(long=real_url).first()
    if found_url:
        return redirect(url_for("display_url",url=found_url.short))
    else:
        short_url = shorten_url()
        new_url = Urls(long=real_url, short=short_url)
        db.session.add(new_url)
        db.session.commit()
        new_search = Urls.query.filter_by(long=real_url).first()
        return redirect(url_for("display_url",url=new_search.short))

# Display the Short Url

@app.route('/display/<url>')
def display_url(url):
    return render_template('shorted.html' , display_url=url)

# Redirect to main Url

@app.route('/<short_url>')
def redirection(short_url):
    long_url = Urls.query.filter_by(short=short_url).first()
    if long_url:
        return redirect(long_url.long)
    else:
        return f'<h1>Url Not Exist</h1>'


if __name__ == '__main__':  #python interpreter assigns "__main__" to the file you run
  app.run(debug=True)
