import bs4 as bs
from urllib2 import urlopen
from models import *

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
