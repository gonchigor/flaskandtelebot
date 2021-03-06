import requests
from bs4 import BeautifulSoup

class BaseAfisha:
    
    def __init__(self):
        r = requests.get(self.url)
        text = r.text
        self.soup = BeautifulSoup(text, 'lxml')

    def __init__(self):
        self.afisha_url = 'https://afisha.tut.by/film/'
        self._last_status = 0

    @property
    def last_status(self):
        return self._last_status
    
    def get_html(self):
        r = requests.get(self.afisha_url)
        self._last_status = r.status_code
        if r.status_code == 200:
            return r.text
        return r.status_code + " " + responses[r.status_code]

    def _get_article(self):
        films = self._get_all_articles()
        for film in films:
            yield film

    def _get_all_articles(self):
        soup = BeautifulSoup(self.get_html(), 'lxml')
        list_films = soup.find('div', id='events-block').find_all('ul', recursive=False)
        films = []
        for f in list_films:
            for article in f.find_all('a', {'class': 'name'}):
                films.append(article.text)
        
        return films

    def get_data(self, num=None):
        texts = self._get_all_articles()
        if num is None:
            return texts
        if len(texts) >= num:
            return texts[num - 1]
        return "Sorry! We don't have so many articles from habr"
    