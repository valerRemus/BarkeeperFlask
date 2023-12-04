from flask_wtf import FlaskForm
from flask_babel import lazy_gettext
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class MessageForm(FlaskForm):
    sender_username = StringField(lazy_gettext('Your Username'), validators=[DataRequired()])
    receiver_username = StringField(lazy_gettext('Recipient Username'), validators=[DataRequired()])
    content = TextAreaField(lazy_gettext('Message'), validators=[DataRequired(), Length(max=128)])
    submit = SubmitField(lazy_gettext('Send Message'))
