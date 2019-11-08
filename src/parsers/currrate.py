import requests
import datetime
from http.client import responses


class BaseCurrRate:
    def __init__(self):
        self.url = 'http://www.nbrb.by/API/ExRates/Rates?Periodicity=0'
    
    def get_data(self, currency=None, *args):
        url_get = self.url
        if len(args) == 1:
            url_get += f'&onDate={args[0].isoformat()}'
        elif len(args) == 3:
            date_iso = self.date_to_iso(*args)
            url_get += f'&onDate={date_iso}'
        try:
            request_rate = requests.get(url_get)
        except ConnectionError:
            return 404
        if request_rate.status_code == 200:
            rates = request_rate.json()
            dict_rates = {rate['Cur_Abbreviation']: (
                rate['Cur_Scale'],
                rate['Cur_Name'],
                rate['Cur_OfficialRate']
                ) for rate in rates}
            if currency is not None:
                return dict_rates[currency.upper()]
            return dict_rates
        return request_rate.status_code

    def get_messages(self, currency=None, *args):
        rates = self.get_data(currency, *args)
        if isinstance(rates, int):
            return rates
        messages = []
        if len(args) == 1:
            text_date = args[0].isoformat()
        elif len(args) == 3:
            text_date = self.date_to_iso(*args)
        else:
            text_date = 'сегодня'
        if isinstance(rates, tuple):
            return ('Курс {1} {2} на {0}: {3}'.format(text_date,
                            *rates),)
        for currate in rates.values():
            messages.append('Курс {1} {2} на {0}: {3}'.format(text_date,
                            *currate))
        return messages

    def _rate_get_date(self, day_=None, month_=None, year_=None):
        if day_ is None and month_ is None and year_ is None:
            return self.rate_url
        in_date = self.date_to_iso(day_, month_, year_)
        add_url = f"&onDate={in_date}"
        return self.rate_url + add_url

    def date_to_iso(self, day_, month_, year_):
        return datetime.date(year_, month_, day_).isoformat()
