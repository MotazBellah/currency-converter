from flask_wtf import FlaskForm
from models import *
from wtforms import StringField, FloatField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError
import datetime

CURRENCY_TYPE = [("EUR","EUR"),("USD","USD"),("JPY","JPY"),("BGN","BGN"),("CZK","CZK"),
                ("GBP","GBP"),("HUF","HUF"),("PLN","PLN"),("RON","RON"),("SEK","SEK"),
                ("CHF","CHF"),("ISK","ISK"),("NOK","NOK"),("HRK","HRK"),("RUB","RUB"),
                ("TRY","TRY"),("AUD","AUD"),("BRL","BRL"),("CAD","CAD"),("CNY","CNY"),
                ("HKD","HKD"),("IDR","IDR"),("ILS","ILS"),("INR","INR"),("KRW","KRW"),
                ("MXN","MXN"),("MYR","MYR"),("NZD","NZD"),("PHP","PHP"),("SGD","SGD"),
                ("THB","THB"),("ZAR","ZAR"),("DKK","DKK")]

# custom validator for the form, to check if date has a valid format and exsit in DB
def date_validate(form, field):
    date_text = field.data
    date_object = CurrencyRate.query.filter_by(time=date_text).first()
    try:
        time = datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValidationError("Incorrect date format, should be YYYY-MM-DD")
    if not date_object:
        raise ValidationError("Incorrect date, Please select another reference date")

class CurrencyCovert(FlaskForm):
    """CurrencyCovert form"""
    # src_currency = StringField('source currency', validators=[InputRequired(message="source currency required"), Length(min=3, max=3, message='currency must be between 3 charachters')])
    src_currency = SelectField('source currency', choices=CURRENCY_TYPE, validators=[InputRequired(message="source currency required")])
    dest_currency = SelectField('destination currency',  choices=CURRENCY_TYPE, validators=[InputRequired(message="source currency required")])
    amount = FloatField('amount', validators=[InputRequired(message="amount required")])
    date = StringField('reference date', validators=[InputRequired(message="reference date required"), date_validate])
