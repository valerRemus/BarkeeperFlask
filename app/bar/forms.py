from app import cocktailRecommender
from flask import session
from flask_wtf import FlaskForm
#from app import cocktailRecommender
from wtforms import RadioField, SubmitField, SelectMultipleField, widgets
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext, gettext


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class EvalForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(EvalForm, self).__init__(*args, **kwargs)
        opinions = [lazy_gettext('Bad'), lazy_gettext('Neutral'), lazy_gettext('Good')]
        op_list = [(x, x) for x in opinions]
        self.option.choices = op_list
    option = RadioField('Label', validators=[DataRequired()])
    submit = SubmitField(lazy_gettext('Submit'))


class SimpleForm(FlaskForm):

    fruits, alco, nonalco, others = cocktailRecommender.get_general_taxonomy()
    fruit_choices = sorted(fruits)
    alco_choices = sorted(alco)
    nonalco_choices = sorted(nonalco)
    others_choices = sorted(others)

    fruit_list = [(x.title(), x.title()) for x in fruits if x != '']
    alco_list = [(x.title(), x.title()) for x in alco if x != '']
    nonalco_list = [(x.title(), x.title()) for x in nonalco if x != '']
    others_list = [(x.title(), x.title()) for x in others if x != '']

    fruits_cb = MultiCheckboxField('Label', choices=fruit_list)
    alco_cb = MultiCheckboxField('Label', choices=alco_list)
    nonalco_cb = MultiCheckboxField('Label', choices=nonalco_list)
    others_cb = MultiCheckboxField('Label', choices=others_list)

    style = {'type': 'button', 'class':'btn btn-default'}
    submit = SubmitField(lazy_gettext('Search'))
