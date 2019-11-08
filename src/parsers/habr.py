import requests
from bs4 import BeautifulSoup
from http.client import responses


class BaseHabr:
    def __init__(self):
        self.habr_url = "https://habr.com/top/monthly/"
        self._last_status = 0

    @property
    def last_status(self):
        return self._last_status
    
    def get_html(self):
        r = requests.get(self.habr_url)
        self._last_status = r.status_code
        if r.status_code == 200:
            return r.text
        return r.status_code + " " + responses[r.status_code]

    def _get_article(self):
        soup = BeautifulSoup(self.get_html, 'lxml')
        for h2 in soup.find_all('article'):
            yield h2.find('h2').a.text

    def _get_all_articles(self):
        soup = BeautifulSoup(self.get_html(), 'lxml')
        return [block.find('h2').a.text for block in soup.find_all('article')]

    def get_data(self, num=None):
        texts = self._get_all_articles()
        if num is None:
            return texts
        if len(texts) >= num:
            return texts[num - 1]
        return "Sorry! We don't have so many articles from habr"
