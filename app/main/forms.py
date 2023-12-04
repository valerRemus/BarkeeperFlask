from flask_wtf import FlaskForm
from flask_babel import lazy_gettext
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class NameForm(FlaskForm):
    name = StringField(lazy_gettext('What is your name?'), validators=[DataRequired()])
    submit = SubmitField(lazy_gettext('Submit'))

class EditProfileForm(FlaskForm):
    name = StringField(lazy_gettext('Real name'), validators=[Length(0, 64)])
    location = StringField(lazy_gettext('Location'), validators=[Length(0, 64)])
    about_me = TextAreaField(lazy_gettext('About me'))
    submit = SubmitField(lazy_gettext('Submit'))
