from flask_wtf import FlaskForm
from models import *
from wtforms import StringField, FloatField
from wtforms.validators import InputRequired, Length


class CurrencyCovert(FlaskForm):
    """CurrencyCovert form"""
    src_currency = StringField('source currency', validators=[InputRequired(message="source currency required"), Length(min=3, max=3, message='currency must be between 3 charachters')])
    dest_currency = StringField('destination currency', validators=[InputRequired(message="destination currency required"), Length(min=3, max=3, message='currency must be between 3 charachters')])
    amount = FloatField('amount', validators=[InputRequired(message="amount required")])
    date = StringField('reference date', validators=[InputRequired(message="reference date required")])
