import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *
from wtform_fields import *


app = Flask(__name__)
app.secret_key = 'super_secret_key'
app.config['WTF_CSRF_SECRET_KEY'] = "b'f\xfa\x8b{X\x8b\x9eM\x83l\x19\xad\x84\x08\xaa"

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///currency.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Currency Convert Form
    conv_form = CurrencyCovert()
    # convert if the validation success
    if conv_form.validate_on_submit():
        src_currency = conv_form.src_currency.data
        dest_currency = conv_form.dest_currency.data
        amount = conv_form.amount.data
        date = conv_form.date.data
        return redirect(url_for('convert', src_currency=src_currency, dest_currency=dest_currency, amount=amount, date=date))

    return render_template('index.html', form=conv_form)


@app.route('/convert')
def convert():
    src_currency = request.args.get('src_currency')
    dest_currency = request.args.get('dest_currency')
    amount = float(request.args.get('amount'))
    date = request.args.get('date')
    # print(amount)
    data = {}
    if dest_currency.lower() == src_currency.lower():
        data['amount'] = round(amount, 4)
        data['currency'] = dest_currency.upper()

    elif src_currency.lower() == 'eur':
        rate = CurrencyRate.query.filter_by(currency=dest_currency).filter_by(time=date).first()
        if rate:
            data['amount'] = round(rate.rate * amount, 4)
            data['currency'] = dest_currency.upper()

    elif dest_currency.lower() == 'eur':
        rate = CurrencyRate.query.filter_by(currency=src_currency).filter_by(time=date).first()
        if rate:
            data['amount'] = round((1 / rate.rate) * amount, 4)
            data['currency'] = dest_currency.upper()

    elif dest_currency.lower() == src_currency.lower():
        data['amount'] = round(amount, 4)
        data['currency'] = dest_currency.upper()

    else:
        des_rate = CurrencyRate.query.filter_by(currency=dest_currency).filter_by(time=date).first()
        src_rate = CurrencyRate.query.filter_by(currency=src_currency).filter_by(time=date).first()
        if des_rate and src_rate:
            print(float(des_rate.rate) / float(src_rate.rate))
            rate = "{:.4f}".format(float(des_rate.rate) / float(src_rate.rate))
            data['amount'] = float(rate) * amount
            data['currency'] = dest_currency.upper()

    return jsonify(data)


# @app.route('/convert/<src_currency>/<dest_currency>/<float:amount>/<date>')
# def convert(src_currency, dest_currency, amount, date):
#     data = {}
#     if src_currency.lower() == 'eur':
#         rate = CurrencyRate.query.filter_by(currency=dest_currency.upper()).filter_by(time=date).first()
#         data['amount'] = rate.rate * amount
#         data['currency'] = dest_currency.upper()
#         print(rate.rate)
#     elif dest_currency.lower() == 'eur':
#         rate = CurrencyRate.query.filter_by(currency=src_currency.upper()).filter_by(time=date).first()
#         data['amount'] = (1 / rate.rate) * amount
#         data['currency'] = dest_currency.upper()
#     else:
#         des_rate = CurrencyRate.query.filter_by(currency=dest_currency.upper()).filter_by(time=date).first()
#         src_rate = CurrencyRate.query.filter_by(currency=src_currency.upper()).filter_by(time=date).first()
#         rate = des_rate.rate / src_rate.rate
#         data['amount'] = rate * amount
#         data['currency'] = dest_currency.upper()
#
#
#     # sorc_curr = CurrencyRate.query.filter_by(currency=src_currency)
#     return jsonify(data)


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 8000))
    app.debug = True
    app.run(host='0.0.0.0', port=PORT)
