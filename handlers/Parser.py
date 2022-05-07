from bs4 import BeautifulSoup
import requests as request


class TelegramParser:
    def __init__(self):
        self.base_url = "https://t.me/"

    def parse_nickname(self, nickname):
        response = request.get(self.base_url + nickname)
        soup = BeautifulSoup(response.text, 'lxml')
        name = soup.find_all('div', {'class': 'tgme_page_title'})
        return len(name)
