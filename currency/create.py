import os
import bs4 as bs
from urllib.request import urlopen
from flask import Flask
from models import *

app = Flask(__name__)

# Configure the sqlalchemy url to get the url
# from heroku if exsit or get the currency.db
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///currency.db')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
# Disable flask_sqlalchemy event system to save memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the app
db.init_app(app)


# Using BeautifulSoup parse the xml file after open and read the url
# Get all the 'cube' tags and load time, currency and rate to DB
def scrap():
    """Function to get the data from the site and loads it to DB"""
    source = urlopen('https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml').read()
    soup = bs.BeautifulSoup(source, 'lxml')
    cube = soup.find('cube').find_all('cube')

    for i in cube:
        if i.has_attr('time'):
            time = i['time']
        if i.has_attr('currency'):
            newCurrency = CurrencyRate(time=time,
                                       currency=i['currency'],
                                       rate=i['rate']
                                       )
            db.session.add(newCurrency)
            db.session.commit()


# create DB and table then load the data into it
def main():
    db.create_all()
    scrap()


if __name__ == "__main__":
    with app.app_context():
        main()
