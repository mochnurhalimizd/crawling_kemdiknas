import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from library.log.lib import LoggerLib
from library.config.lib import get_config
from library.request.lib import RequestLib
from library.bs4.lib import BeautifulSoupLib
from library.thread.lib import ThreadLib

from model.detail import DetailModel


class DetailBS4Modules:
    def __init__(self):
        self.logger = LoggerLib('detailbs4_modules')
        self.request = RequestLib(self.logger)
        self.config = get_config('config.conf')
        self.model = DetailModel(self.get_parameter(self.config).get('database'), self.logger)
        self.data = self.get_parameter(self.config)
        self.required = [
            'profil',
            'kontak',
        ]

    def run(self):
        for data in self.model.get_data().get('data'):
            thread = ThreadLib(1, 'hello', callback=self.get_element, param=data)
            thread.start()

    def get_element(self, data):
        url = 'http://dapo.dikdasmen.kemdikbud.go.id/sekolah/{}'.format(data.get('sekolah_id_enkrip'))
        element = BeautifulSoupLib(url, self.logger)

        response = {}
        response.update({'info': self.get_profile(element)})

        for key in self.required:
            item = element.find('#{}'.format(key), child=0)
            child = element.find('.col-md-6', element=item)

            temp = [self.get_detail(element, x) for x in child]
            response.update({key: temp})

        self.model.search_data(data.get('sekolah_id_enkrip'), {'info_sekolah': response})

    def get_profile(self, element):
        temp = [self.parse_detail(x) for x in element.find('.profile-usermenu > ul > li > a')]
        return {k: v for x in temp for k, v in x.items()}

    def get_detail(self, element, item):
        temp = {}
        temp.update({'key': element.find('.panel-heading', child=0, element=item).get_text().strip().lower()})

        value = [self.parse_detail(x) for x in element.find('.panel-body > p', element=item)]
        temp.update({'value': {k: v for x in value for k, v in x.items()}})
        return temp

    @staticmethod
    def parse_detail(item):
        temp = [x.strip().lower() for x in item.get_text().strip().split(':')]
        return {temp[0]: temp[1]}

    @staticmethod
    def get_parameter(config):
        return {
            'url': config.get('url', 'get_location'),
            'database': {
                'db': config.get('mongo', 'mongo_database_config'),
                'host': config.get('mongo', 'mongo_url'),
                'port': config.get('mongo', 'mongo_port')
            }
        }


if __name__ == '__main__':
    a = DetailBS4Modules()
    a.run()
