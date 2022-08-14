from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.widgets import TextArea

from blog.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=30,
                                                                          message="Please enter a username correctly")])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5)])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password',
                                                                                    message="Please enter a password "
                                                                                            "equal to this "
                                                                                            "passwordField")])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already exist')

    def validate_email(self, email):
        user = User.query.filter_by(username=email.data).first()
        if user:
            raise ValidationError('This email is already exist')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember')


class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=30,
                                                                          message="Please enter a username correctly")])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5)])

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username is already exist')
        else:
            raise ValidationError('This username is already exist')


class PostForm(FlaskForm):
    title = StringField('title', validators=[DataRequired(), Length(min=5)])
    content = TextAreaField('content', validators=[DataRequired(), Length(min=10)])
