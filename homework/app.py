import hashlib

from flask import Flask, redirect, url_for, render_template, request
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from homework.models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'GHFJTFF5JYjd55r678888y8hug55e55ehrdjt'
csrf = CSRFProtect(app)
db.init_app(app)


@app.cli.command('init-db')
def init_db():
    db.create_all()


def containsDigitValidator(form, password):
    if not any(c.isdigit() for c in password.data):
        raise ValidationError('must contain at least one digit')


def containsLetterValidator(form, password):
    if not any(c.isalpha() for c in password.data):
        raise ValidationError('must contain at least one letter')


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8),
                                                     containsLetterValidator,
                                                     containsDigitValidator])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        surname = form.surname.data
        email = form.email.data
        password = hashlib.md5(form.password.data.encode()).hexdigest()
        new_user = User(firstname=name,
                        lastname=surname,
                        email=email,
                        password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('success'))
    return render_template('index.html', form=form)


@app.route('/success/')
def success():
    users = User.query.all()
    context = {
        'title': 'Пользователи',
        'users': users}
    return render_template('success.html', **context)


@app.route('/users/')
def all_users():
    users = User.query.all()
    context = {
        'title': 'Пользователи',
        'users': users}
    return render_template('users.html', **context)
