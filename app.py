from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from data import Articles
from flask_mysql_connector import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

Articles = Articles()

app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DATABASE'] = 'myflaskapp'
app.config['MYSQL_PASSWORD'] = 'IsakonIsakon123'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/article/<string:id>/')
def article(id):
    return render_template("articles.html", id=id)

@app.route('/login')
def login():
    return render_template("login.html")

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=1, max=50)])
    email = StringField('Email', [validators.Length(min=1, max=50)])
    password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Пароли не совпадают')])
    confirm =PasswordField('Confirm password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        try:
            con = mysql.connection
            cursor = con.cursor()
            cursor.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))
            con.commit()
            cursor.close()
        except BaseException as e:
            return "there is a problem with DB"
        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template("register.html", form=form)

if __name__ == '__main__':
    app.secret_key = 'my_terrible_secret'
    app.run(debug=True)