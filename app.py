import os
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SECRET_KEY'] = 'medisha@3.com!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///OSUSU.db'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

app.app_context().push()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(25))
    middleName = db.Column(db.String(25))
    lastName = db.Column(db.String(25))
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    phoneNumber = db.Column(db.Integer, unique=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginForm(FlaskForm):
    username = StringField('username', validators=[
                           InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[
                             InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    firstName = StringField('First Name', validators=[InputRequired(), Length(max=25)])
    middleName = StringField('Middle Name', validators=[InputRequired(), Length(max=25)])
    lastName = StringField('last Name', validators=[InputRequired(), Length(max=25)])
    email = StringField('email', validators=[InputRequired(), Email(
        message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[
                           InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[
                             InputRequired(), Length(min=8, max=80)])
    phoneNumber = StringField('Phone number', validators=[InputRequired(), Length(min=12, max=14)])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'
        # return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(firstName=form.firstName.data, middleName=form.middleName.data, lastName=form.lastName.data,
                        username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
        # return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/addCustomer')
def addCustomer():
    return render_template('addCustomer.html', name=current_user.username)

@app.route('/chat')
def Chat():
    return render_template('chat.html', name=current_user.username)

@app.route('/contribution')
def Contribution():
    return render_template('contribution.html', name=current_user.username)

@app.route('/group')
def Group():
    return render_template('group.html', name=current_user.username)

@app.route('/collection')
def Collection():
    return render_template('collection.html', name=current_user.username)


if __name__ == '__main__':
    app.run(debug=True)
