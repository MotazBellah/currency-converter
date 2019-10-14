import bs4 as bs
from urllib.request import urlopen
from flask import Flask
from models import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///currency.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db.init_app(app)

def scrap():
    source = urlopen('https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml').read()
    soup = bs.BeautifulSoup(source,'lxml')
    # cube = soup.find('cube').find_all('cube')
    cube = soup.find('cube').find_all('cube')

    for i in cube:
        if i.has_attr('time'):
            time = i['time']
        if i.has_attr('currency'):
            newCurrency = CurrencyRate(time=time, currency=i['currency'], rate=i['rate'])
            db.session.add(newCurrency)
            db.session.commit()


def main():
    db.create_all()
    scrap()


if __name__ == "__main__":
    with app.app_context():
        main()
