from flask_wtf import FlaskForm
from flask_babel import gettext, lazy_gettext
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError

from app.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
        Email()])
    password = PasswordField(lazy_gettext('Password'), validators=[DataRequired()])
    remember_me = BooleanField(lazy_gettext('Keep me logged in'))
    submit = SubmitField(lazy_gettext('Log In'))


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
        Email()])
    username = StringField(lazy_gettext('Username'), validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               lazy_gettext('Usernames must have only letters, numbers, dots or '
               'underscores'))])
    password = PasswordField(lazy_gettext('Password'), validators=[
        DataRequired(), EqualTo('password2', message=lazy_gettext('Passwords must match.')),
    Length(min=8, max=64, message=lazy_gettext('Password length must be between 8 and 64 characters.'))])
    password2 = PasswordField(lazy_gettext('Confirm password'), validators=[DataRequired()])
    submit = SubmitField(lazy_gettext('Register'))

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(gettext('Email already registered.'))

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(gettext('Username already in use.'))



class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    submit = SubmitField(lazy_gettext('Reset Password'))



class PasswordResetForm(FlaskForm):
    password = PasswordField(lazy_gettext('New Password'), validators=[
        DataRequired(), EqualTo('password2', message=lazy_gettext('Passwords must match'))])
    password2 = PasswordField(lazy_gettext('Confirm password'), validators=[DataRequired()])
    submit = SubmitField(lazy_gettext('Reset Password'))



class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(lazy_gettext('Old password'), validators=[DataRequired()])
    password = PasswordField(lazy_gettext('New password'), validators=[
        DataRequired(), EqualTo('password2', message=lazy_gettext('Passwords must match.'))])
    password2 = PasswordField(lazy_gettext('Confirm new password'),
                              validators=[DataRequired()])
    submit = SubmitField(lazy_gettext('Update Password'))
