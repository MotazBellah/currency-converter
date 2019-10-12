from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class CurrencyRate(db.Model):
    __tablename__ = 'currency-rate'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String)
    currency = db.Column(db.String)
    rate = db.Column(db.Float, default=0.0)
