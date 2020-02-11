from flask_wtf import Form
from_bcrypt import check_password_hash
from models import User
from wtforms import PasswordField, StringField, TextAreaField
from wtforms.validators import DataRequired, Regexp, Email, Length, EqualTo


def name_exist(form, field):
    if user.select().where(user.username ==field.data).exists():
        raise ValidationError('User with that name already exists')

def email_exists(form, field):
    if user.select().where(user.email ==field.data).exists():
        raise ValidationError('User with that email already exists')



class registerform(Form):
    username = StringFeild(
        'Username', 
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=("Username should be one word, letters"
                            "numbers, and underscores only")
            ),
            name_exists
        ])
        email = stringField(
            'Email', 
            validators=[
                DatarRequired(), 
                Email(),
                email_exists
            ])
        password = PasswordField(
            'Password',
            validators=[
                DataRequired(),
                Length(min=8)
                EqualTo('password2', message='Passwords must match')
            ])

        password2 = PasswordField(
            'Confirm Password',
            validators=[DataRequired()]
        )


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class Postform(Form):
    content = TextAreaField("whats Up!", validators=[DataRequired()])
