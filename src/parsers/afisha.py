import requests
from bs4 import BeautifulSoup

class Afisha:
    url = 'https://afisha.tut.by/film/'
    
    def __init__(self):
        r = requests.get(self.url)
        text = r.text
        self.soup = BeautifulSoup(text, 'lxml')
    