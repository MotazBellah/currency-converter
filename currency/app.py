import os
import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import *
from wtform_fields import *


app = Flask(__name__)
app.secret_key = os.urandom(12).hex()
# set secret key to cross site requset forgery
# to generate a token when WTF submitted
app.config['WTF_CSRF_SECRET_KEY'] = "b'f\xfa\x8b{X\x8b\x9eM\x83l\x19\xad\x84\x08\xaa"

# Configure the sqlalchemy url to get the url
# from heroku if exsit or get the currency.db
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///currency.db')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
# Disable flask_sqlalchemy event system to save memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Main route display the form with get requset
# redirect to convert route with post request
@app.route('/', methods=['GET', 'POST'])
def index():
    # get Currency Convert Form from WTF
    conv_form = CurrencyCovert()
    # convert if the validation success
    if conv_form.validate_on_submit():
        # Get the data from the form field
        src_currency = conv_form.src_currency.data
        dest_currency = conv_form.dest_currency.data
        amount = conv_form.amount.data
        date = conv_form.date.data
        # redirect to convert route
        # Pass the form's data as a parameter to convert route
        return redirect(url_for('convert',
                                src_currency=src_currency,
                                dest_currency=dest_currency,
                                amount=amount,
                                date=date))

    return render_template('index.html', form=conv_form)


# Get the data from the URL
# Accept only get request
@app.route('/convert', methods=['GET'])
def convert():
    src_currency = request.args.get('src_currency').upper()
    dest_currency = request.args.get('dest_currency').upper()
    amount = float(request.args.get('amount'))
    date = request.args.get('date')
    # Get the destination row from DB
    # filter by the dest_currency and date
    des_rate = (CurrencyRate.query.filter_by(currency=dest_currency)
                                  .filter_by(time=date)
                                  .first())
    # Get the source row from DB
    # filter by the source_currency and date
    src_rate = (CurrencyRate.query.filter_by(currency=src_currency)
                                  .filter_by(time=date)
                                  .first())
    # Declare the data dict
    data = {}
    # Make sure the date in the format YYYY-MM-DD
    # else return empty JSON
    try:
        time = datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return jsonify(data)
    # check id dest and src currency are equel
    if dest_currency.lower() == src_currency.lower():
        data['amount'] = round(amount, 4)
        data['currency'] = dest_currency
    # If the src is eur, get the rate from dest row
    elif src_currency == 'EUR':
        if des_rate:
            data['amount'] = round(des_rate.rate * amount, 4)
            data['currency'] = dest_currency
    # If the dest is eur, get the inverse of the src row
    elif dest_currency == 'EUR':
        if src_rate:
            data['amount'] = round((1 / src_rate.rate) * amount, 4)
            data['currency'] = dest_currency
    # otherwise, divide the des_rate by src_rate
    # to get the rate between des and src
    else:
        if des_rate and src_rate:
            rate = "{:.4f}".format(float(des_rate.rate) / float(src_rate.rate))
            data['amount'] = float(rate) * amount
            data['currency'] = dest_currency
    # return data in Json form
    return jsonify(data)


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 7000))
    app.debug = True
    app.run(host='0.0.0.0', port=PORT)
