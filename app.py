import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *


app = Flask(__name__)
app.secret_key = 'super_secret_key'
app.config['WTF_CSRF_SECRET_KEY'] = "b'f\xfa\x8b{X\x8b\x9eM\x83l\x19\xad\x84\x08\xaa"

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///currency.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 8000))
    app.debug = True
    app.run(host='0.0.0.0', port=PORT)
