import requests
import flask


class NBRB:
    url = 'http://www.nbrb.by/API/ExRates/Rates?Periodicity=0'
    
    def rate(self, currency=None, date_value=None):
        url_get = self.url
        if date_value is not None:
            url_get += f'&onDate={date_value.isoformat()}'
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
