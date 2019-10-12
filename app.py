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
        return redirect(url_for('convert'))

    return render_template('index.html', form=conv_form)

@app.route('/convert')
def convert():
    return 'hi'


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 8000))
    app.debug = True
    app.run(host='0.0.0.0', port=PORT)
