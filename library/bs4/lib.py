import requests
from bs4 import BeautifulSoup


class BeautifulSoupLib:
    def __init__(self, url, logger):
        self.logger = logger
        self.element = None
        self.get_request(url)

    def get_request(self, url):
        self.element = BeautifulSoup(self.get_html(url), 'html.parser')
        return self.element

    def find(self, css_path, child=None, element=None):
        temp = None

        if element is not None:
            temp = element.select(css_path)
        else:
            temp = self.element.select(css_path)

        if child is not None:
            return temp[child]
        else:
            return temp

    def get_html(self, url):
        try:
            request = requests.get(url)
            return request.text
        except requests.exceptions.RequestException:
            return self.get_html(url)
